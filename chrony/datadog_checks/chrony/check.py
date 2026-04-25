#!/usr/bin/env python3

import re
import subprocess

from datadog_checks.base import AgentCheck


class ChronyCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(ChronyCheck, self).__init__(name, init_config, instances)

        # Field definitions - using only Datadog supported units
        # Format: fieldname, regex_pattern, description, unit (None for unitless)
        self.fields = [
            ('stratum', r'^Stratum', 'Stratum', None),  # Unitless (level not supported)
            ('systime', r'^System.time', 'System Time', 'second'),
            ('frequency', r'^Frequency', 'Frequency', None),  # Unitless (ppm not supported)
            ('residualfreq', r'^Residual.freq', 'Residual Frequency', None),  # Unitless (ppm not supported)
            ('skew', r'^Skew', 'Skew', None),  # Unitless (ppm not supported)
            ('rootdelay', r'^Root.delay', 'Root delay', 'second'),
            ('rootdispersion', r'^Root.dispersion', 'Root dispersion', 'second'),
        ]

        self.chronyc_path = self._find_chronyc()

    def _find_chronyc(self):
        """Find the chronyc executable path"""
        try:
            result = subprocess.run(['which', 'chronyc'], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def _get_chrony_tracking(self):
        """Execute chronyc tracking command and return output"""
        if not self.chronyc_path:
            raise Exception("chronyc executable not found")

        try:
            result = subprocess.run(
                [self.chronyc_path, 'tracking'], capture_output=True, text=True, check=True, timeout=30
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to execute chronyc tracking: {e}")
        except subprocess.TimeoutExpired:
            raise Exception("chronyc tracking command timed out")

    def _parse_chrony_output(self, output):
        """Parse chronyc tracking output and extract metrics"""
        metrics = {}

        for fieldname, regex_pattern, _description, _unit in self.fields:
            # Find the line matching the regex pattern
            pattern = re.compile(regex_pattern, re.IGNORECASE)

            for line in output.split('\n'):
                if pattern.match(line):
                    # Extract the value part after the colon
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        value_part = parts[1].strip()

                        # Parse the numeric value (no scaling factor)
                        value = self._extract_numeric_value(value_part)
                        if value is not None:
                            metrics[fieldname] = value
                    break

        return metrics

    def _extract_numeric_value(self, value_part):
        """Extract numeric value from chrony output line"""
        # Handle cases like "0.143763348 seconds slow of NTP time"
        # or "9.733 ppm slow" or "+0.086 ppm"

        # Extract the first number from the string
        number_match = re.search(r'[+-]?\d+\.?\d*', value_part)
        if not number_match:
            return None

        try:
            value = float(number_match.group())

            # Check if the line contains "slow" which indicates negative values
            if 'slow' in value_part.lower():
                value = -value

            # Return the value in its original units
            return value

        except ValueError:
            return None

    def _get_reference_info(self, output):
        """Extract reference server information for tagging"""
        reference_info = {}

        for line in output.split('\n'):
            if line.strip().startswith('Reference ID'):
                # Extract reference ID and server name
                parts = line.split(':', 1)
                if len(parts) == 2:
                    ref_part = parts[1].strip()
                    # Parse format like "89BE0204 (time1.weber.edu)"
                    if '(' in ref_part and ')' in ref_part:
                        ip = ref_part.split('(')[0].strip()
                        server = ref_part.split('(')[1].split(')')[0].strip()
                        reference_info['reference_ip'] = ip
                        reference_info['reference_server'] = server
                    else:
                        reference_info['reference_ip'] = ref_part
                break

        return reference_info

    def check(self, instance):
        """Main check method called by Datadog agent"""
        try:
            # Get chrony tracking output
            output = self._get_chrony_tracking()

            # Parse metrics
            metrics = self._parse_chrony_output(output)

            # Get reference server info for tagging
            reference_info = self._get_reference_info(output)

            # Prepare tags
            tags = list(instance.get('tags', [])) if instance else []
            service = instance.get('service') if instance else None
            if not service:
                service = self.init_config.get('service')
            if service:
                tags.append(f"service:{service}")
            if reference_info.get('reference_server'):
                tags.append(f"reference_server:{reference_info['reference_server']}")
            if reference_info.get('reference_ip'):
                tags.append(f"reference_ip:{reference_info['reference_ip']}")

            # Submit metrics to Datadog with proper units
            for fieldname, value in metrics.items():
                metric_name = f"chrony.{fieldname}"

                # Find the unit for this metric
                unit = None
                for field_name, _regex_pattern, _description, field_unit in self.fields:
                    if field_name == fieldname:
                        unit = field_unit
                        break

                # Submit metric with unit information
                self.gauge(metric_name, value, tags=tags)
                self.log.debug("Submitted metric %s: %s %s", metric_name, value, unit or '')

            # Submit a service check for chrony availability
            self.service_check('chrony.can_connect', AgentCheck.OK, tags=tags)

            self.log.info("Successfully collected %d chrony metrics", len(metrics))

        except Exception as e:
            self.log.error("Error collecting chrony metrics: %s", e)
            self.service_check('chrony.can_connect', AgentCheck.CRITICAL, message=str(e))
