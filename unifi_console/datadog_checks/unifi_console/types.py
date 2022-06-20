from datadog_checks.unifi_console.mertrics import Gauge


class APIConnectionError(Exception):
    pass


class ControllerInfo(object):
    def __init__(self, about_info) -> None:
        self.up = about_info["meta"]["up"]
        self.version = about_info["meta"]["server_version"]
        self.uuid = about_info["meta"]["uuid"]

        self.fullName = "Unifi Controller {} uuid: {}".format(self.version, self.uuid)


class DeviceInfo(object):
    def __init__(self, device_info) -> None:
        id = device_info["_id"]
        architecture = device_info["architecture"]
        kernel_version = device_info["kernel_version"]
        model = device_info["model"]
        name = device_info["name"]
        version = device_info["version"]
        state = device_info["state"]
        uptime = device_info["uptime"]
        clients = device_info["num_sta"]
        satisfaction = device_info["satisfaction"]
        system_cpu_pct = device_info["system-stats"]["cpu"]
        system_mem_used = device_info["sys_stats"]["mem_used"]
        system_mem_total = device_info["sys_stats"]["mem_total"]
        system_mem_buffer = device_info["sys_stats"]["mem_buffer"]
        system_mem_pct = device_info["system-stats"]["mem"]

        self.tags = []
        self.tags.append("id:{}".format(id))
        self.tags.append("architecture:{}".format(architecture))
        self.tags.append("kernel_version:{}".format(kernel_version))
        self.tags.append("model:{}".format(model))
        self.tags.append("device:{}".format(name))
        self.tags.append("device_version:{}".format(version))

        self.metrics = []
        self.metrics.append(Gauge("device.status", state, self.tags))
        self.metrics.append(Gauge("device.uptime", uptime, self.tags))
        self.metrics.append(Gauge("device.clients", clients, self.tags))
        self.metrics.append(Gauge("device.satisfaction", satisfaction, self.tags))
        self.metrics.append(Gauge("device.system.cpu.pct", system_cpu_pct, self.tags))
        self.metrics.append(Gauge("device.system.mem.used", system_mem_used, self.tags))
        self.metrics.append(Gauge("device.system.mem.total", system_mem_total, self.tags))
        self.metrics.append(Gauge("device.system.mem.buffer", system_mem_buffer, self.tags))
        self.metrics.append(Gauge("device.system.mem.pct", system_mem_pct, self.tags))
        self.metrics.append(Gauge("device.tx_packets", device_info['stat']['ap']['tx_packets'], self.tags))
        self.metrics.append(Gauge("device.tx_bytes", device_info['stat']['ap']['tx_bytes'], self.tags))
        self.metrics.append(Gauge("device.tx_errors", device_info['stat']['ap']['tx_errors'], self.tags))
        self.metrics.append(Gauge("device.tx_dropped", device_info['stat']['ap']['tx_dropped'], self.tags))
        self.metrics.append(Gauge("device.tx_retries", device_info['stat']['ap']['tx_retries'], self.tags))
        self.metrics.append(Gauge("device.rx_packets", device_info['stat']['ap']['rx_packets'], self.tags))
        self.metrics.append(Gauge("device.rx_bytes", device_info['stat']['ap']['rx_bytes'], self.tags))
        self.metrics.append(Gauge("device.rx_errors", device_info['stat']['ap']['rx_errors'], self.tags))
        self.metrics.append(Gauge("device.rx_dropped", device_info['stat']['ap']['rx_dropped'], self.tags))
        self.metrics.append(Gauge("device.guests", device_info['guest-num_sta'], self.tags))
