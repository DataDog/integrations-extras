from checks import AgentCheck
from datetime import tzinfo, timedelta
import datetime
import requests
import json
import calendar

class UTC(tzinfo):
  def utcoffset(self, dt):
    return timedelta(0)
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return timedelta(0)

class WinDocker(AgentCheck):
	def check(self, instance):
		container_full_ids = []
		container_ids = []
		container_urls = []
		id_tag = ""
		image_tag = ""
		state_tag = ""
		status_tag = ""
		name_tag = ""
		net_tmpl = "docker.windows.networks.{}"
		blkio_stats_tmpl = "docker.windows.blkio_stats.{}"
		storage_stats_tmpl = "docker.windows.storage_stats.{}"
		cpu_stats_tmpl = "docker.windows.cpu_stats.cpu_usage.{}"
		throttling_data_tmpl = "docker.windows.cpu_stats.throttling_data.{}"
		precpu_stats_cpu_usage_tmpl = "docker.windows.precpu_stats.cpu_usage.{}"
		precpu_stats_throttling_data_tmpl = "docker.windows.precpu_stats.throttling_data.{}"
		memory_stats_tmpl = "docker.windows.memory_stats.{}"

		container_url="http://localhost:2375/containers/json"
		containers_response = requests.get(container_url, timeout=1).json()


		for value in containers_response:
			container_full_ids.append(value["Id"])
			container_count = len(containers_response)
			
			if value:
				id_tag = "sources:docker_win"
				image_tag = "docker_image:" + value["Image"]
				state_tag = "state:" + value["State"]
				status_tag = "status:" + value["Status"]
				name_tag = "container_name:" + value["Names"][0]
				self.gauge("docker.windows.created", value["Created"], tags=[id_tag, image_tag, name_tag, status_tag, state_tag ])
	# running containers:
		self.gauge("docker.windows.containers.running", container_count, tags=[id_tag, image_tag, name_tag, status_tag, state_tag])

		for x in container_full_ids:
			container_urls.append("http://localhost:2375/containers/" + x + "/stats")
			container_ids.append(x[:12])

		for index, value in enumerate(container_urls):
			cont_health_response = requests.get(value, stream=True)
			for raw_stream in cont_health_response.iter_lines():
				short_container_id = "container_id:"+ container_ids[index]
				if raw_stream:
					#main stream
					try:
						rs = json.loads(raw_stream)
					except:
						print("Error loading JSON")
						break
				#read:
					read_date_parts = rs['read'].split('.')
					d = datetime.datetime.strptime(read_date_parts[0], '%Y-%m-%dT%H:%M:%S')
					microseconds = int(int(read_date_parts[1].rstrip('Z'))/1000.0)
					d = d.replace(microsecond=microseconds, tzinfo=UTC())
					d = calendar.timegm(d.timetuple())
					self.gauge('docker.windows.read_at',d,tags=[short_container_id,id_tag, image_tag, name_tag, status_tag, state_tag])

				#num_proces:
					num_procs=rs['num_procs']
					self.gauge('docker.windows.num_proces',num_procs, tags=[short_container_id,id_tag, image_tag, name_tag, status_tag, state_tag])

				#blkio_stats:
					blkio_stats=rs['blkio_stats']
					for blkio_stats_prop in ["io_service_bytes_recursive", "io_serviced_recursive", "io_queue_recursive", "io_service_time_recursive", "io_wait_time_recursive","io_merged_recursive", "io_time_recursive", "sectors_recursive"]:
						self.gauge(blkio_stats_tmpl.format(blkio_stats_prop), blkio_stats[blkio_stats_prop], tags=[short_container_id,id_tag, image_tag, name_tag, status_tag, state_tag])

				#storage_stats:
					storage_stats=rs['storage_stats']
					for storage_stats_prop in ["read_count_normalized","read_size_bytes","write_count_normalized","write_size_bytes"]:
						self.gauge(storage_stats_tmpl.format(storage_stats_prop), storage_stats[storage_stats_prop], tags=[short_container_id,id_tag, image_tag, name_tag, status_tag, state_tag])

				#cpu_stats:
					cpu_usage=rs['cpu_stats']['cpu_usage']
					for cpu_stat_prop in ["total_usage", "usage_in_kernelmode", "usage_in_usermode"]:
						self.gauge(cpu_stats_tmpl.format(cpu_stat_prop), cpu_usage[cpu_stat_prop], tags=[short_container_id,id_tag, image_tag, name_tag, status_tag, state_tag])

					throttling_data=rs['cpu_stats']['throttling_data']
					for throttling_data_prop in ["periods","throttled_periods","throttled_time"]:
						self.gauge(throttling_data_tmpl.format(throttling_data_prop), throttling_data[throttling_data_prop], tags=[short_container_id,id_tag, image_tag, name_tag, status_tag, state_tag])

				#precpu_stats:
					precpu_stats=rs['precpu_stats']['cpu_usage']
					for precpu_prop in ["total_usage", "usage_in_kernelmode", "usage_in_usermode"]:
						self.gauge(precpu_stats_cpu_usage_tmpl.format(precpu_prop), precpu_stats[precpu_prop], tags=[short_container_id,id_tag, image_tag, name_tag, status_tag, state_tag])
					
					precpu_throttling_data=rs['precpu_stats']['throttling_data']
					for precpu_throttling_prop in ["periods", "throttled_periods", "throttled_time"]:
						self.gauge(precpu_stats_throttling_data_tmpl.format(precpu_throttling_prop), precpu_throttling_data[precpu_throttling_prop], tags=[short_container_id,id_tag, image_tag, name_tag, status_tag, state_tag])

				#memory_stats:
					memory_stats=rs['memory_stats']
					for memory_stat_prop in ["commitbytes", "commitpeakbytes", "privateworkingset"]:
						self.gauge(memory_stats_tmpl.format(memory_stat_prop), memory_stats[memory_stat_prop], tags=[short_container_id,id_tag, image_tag, name_tag, status_tag, state_tag])

				#networks:
					networks=rs['networks']
					for guid, data in networks.iteritems():
						guid_tag = "guid:" + guid
						for prop in ["rx_bytes", "rx_packets", "rx_errors", "rx_dropped", "tx_bytes", "tx_packets", "tx_errors", "tx_dropped"]:
							self.gauge(net_tmpl.format(prop), data[prop], tags=[short_container_id, guid_tag,id_tag, image_tag, name_tag, status_tag, state_tag])

				break