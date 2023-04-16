import json

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException
from datadog_checks.base.utils.common import round_value as round
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

EXPECTED_RESPONSE_CODE = "NO_ERROR"
CHROME_FLAGS = ['--headless']


class LighthouseCheck(AgentCheck):
    def check(self, instance):
        backward_compatible_lighthouse_url = instance.get('url')
        lighthouse_urls = instance.get('urls', [])
        lighthouse_name = instance.get('name')
        extra_chrome_flags = instance.get('extra_chrome_flags', [])
        form_factor = instance.get('form_factor')

        if backward_compatible_lighthouse_url:
            lighthouse_urls.append(backward_compatible_lighthouse_url)

        if not lighthouse_urls or not lighthouse_name:
            self.log.error("missing instance url or name")
            raise CheckException("missing lighthouse instance url or name, please fix yaml")

        for lighthouse_url in lighthouse_urls:
            cmd = [
                "lighthouse",
                lighthouse_url,
                "--output",
                "json",
                "--quiet",
                "--chrome-flags='{}'".format(" ".join(CHROME_FLAGS + extra_chrome_flags)),
            ]

            if form_factor:
                cmd.append("--form-factor=" + form_factor)
                if form_factor == "desktop":
                    cmd.append("--preset=desktop")

            json_string, error_message, exit_code = LighthouseCheck._get_lighthouse_report(cmd, self.log, False)

            # check for error since we have raise_on_empty_output set to False
            if exit_code > 0:
                self.log.error(
                    "lighthouse subprocess error %s exit code %s for url: %s", error_message, exit_code, lighthouse_url
                )
                raise CheckException(json_string, error_message, exit_code)

            try:
                data = json.loads(json_string)
            except Exception as e:
                self.log.warning("lighthouse response JSON different than expected for url: %s", lighthouse_url)
                raise CheckException(error_message, exit_code, e)

            if data.get("runtimeError", {"code": EXPECTED_RESPONSE_CODE}).get("code") == EXPECTED_RESPONSE_CODE:
                score_accessibility = round(
                    ((data.get("categories", {}).get("accessibility", {}).get("score") or 0) * 100)
                )
                score_best_practices = round(
                    ((data.get("categories", {}).get("best-practices", {}).get("score") or 0) * 100)
                )
                score_performance = round(((data.get("categories", {}).get("performance", {}).get("score") or 0) * 100))
                score_pwa = round(((data.get("categories", {}).get("pwa", {}).get("score") or 0) * 100))
                score_seo = round(((data.get("categories", {}).get("seo", {}).get("score") or 0) * 100))
                largest_contentful_paint = LighthouseCheck._get_numeric_audit_value(data, "largest-contentful-paint")
                first_contentful_paint = LighthouseCheck._get_numeric_audit_value(data, "first-contentful-paint")
                cumulative_layout_shift = LighthouseCheck._get_numeric_audit_value(data, "cumulative-layout-shift")
                max_potential_fid = LighthouseCheck._get_numeric_audit_value(data, "max-potential-fid")
                time_to_interactive = LighthouseCheck._get_numeric_audit_value(data, "interactive")
                mainthread_work_breakdown = LighthouseCheck._get_numeric_audit_value(data, "mainthread-work-breakdown")
                unused_javascript = LighthouseCheck._get_numeric_audit_value(data, "unused-javascript")
                unused_css_rules = LighthouseCheck._get_numeric_audit_value(data, "unused-css-rules")
                modern_image_formats = LighthouseCheck._get_numeric_audit_value(data, "modern-image-formats")
                uses_optimized_images = LighthouseCheck._get_numeric_audit_value(data, "uses-optimized-images")
                render_blocking_resources = LighthouseCheck._get_numeric_audit_value(data, "render-blocking-resources")
                bootup_time = LighthouseCheck._get_numeric_audit_value(data, "bootup-time")
                server_response_time = LighthouseCheck._get_numeric_audit_value(data, "server-response-time")
                speed_index = LighthouseCheck._get_numeric_audit_value(data, "speed-index")
                dom_size = LighthouseCheck._get_numeric_audit_value(data, "dom-size")
                total_blocking_time = LighthouseCheck._get_numeric_audit_value(data, "total-blocking-time")
            else:
                err_code = data.get("runtimeError", {}).get("code")
                err_msg = data.get("runtimeError", {}).get("message")
                self.log.warning(
                    "not collecting lighthouse metrics for url %s runtimeError code %s message %s",
                    lighthouse_url,
                    err_code,
                    err_msg,
                )
                return
            # add tags

            tags = instance.get('tags', [])
            if type(tags) != list:
                self.log.warning('The tags list in the lighthouse check is not configured properly')
                tags = []

            tags.append("url:{0}".format(lighthouse_url))
            tags.append("name:{0}".format(lighthouse_name))

            self.gauge("lighthouse.accessibility", score_accessibility, tags=tags)
            self.gauge("lighthouse.best_practices", score_best_practices, tags=tags)
            self.gauge("lighthouse.performance", score_performance, tags=tags)
            self.gauge("lighthouse.pwa", score_pwa, tags=tags)
            self.gauge("lighthouse.seo", score_seo, tags=tags)
            self.gauge("lighthouse.largest_contentful_paint", largest_contentful_paint, tags=tags)
            self.gauge("lighthouse.first_contentful_paint", first_contentful_paint, tags=tags)
            self.gauge("lighthouse.cumulative_layout_shift", cumulative_layout_shift, tags=tags)
            self.gauge("lighthouse.max_potential_fid", max_potential_fid, tags=tags)
            self.gauge("lighthouse.time_to_interactive", time_to_interactive, tags=tags)
            self.gauge("lighthouse.mainthread_work_breakdown", mainthread_work_breakdown, tags=tags)
            self.gauge("lighthouse.unused_javascript", unused_javascript, tags=tags)
            self.gauge("lighthouse.unused_css_rules", unused_css_rules, tags=tags)
            self.gauge("lighthouse.modern_image_formats", modern_image_formats, tags=tags)
            self.gauge("lighthouse.uses_optimized_images", uses_optimized_images, tags=tags)
            self.gauge("lighthouse.render_blocking_resources", render_blocking_resources, tags=tags)
            self.gauge("lighthouse.bootup_time", bootup_time, tags=tags)
            self.gauge("lighthouse.server_response_time", server_response_time, tags=tags)
            self.gauge("lighthouse.speed_index", speed_index, tags=tags)
            self.gauge("lighthouse.dom_size", dom_size, tags=tags)
            self.gauge("lighthouse.total_blocking_time", total_blocking_time, tags=tags)

    @staticmethod
    def _get_lighthouse_report(command, logger, raise_on_empty=False):
        json, err_msg, exit_code = get_subprocess_output(command, logger, raise_on_empty_output=raise_on_empty)
        return json, err_msg, exit_code

    @staticmethod
    def _get_numeric_audit_value(data, attribute):
        return data.get("audits", {}).get(attribute, {}).get("numericValue") or 0
