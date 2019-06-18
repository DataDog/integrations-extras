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

class DockerConstant:
# Metric Name Schema
	NET_TMPL = "docker.networks.{}"
	BLKIO_STATS_TMPL = "docker.blkio_stats.{}"
	STORAGE_STATS_TMPL = "docker.storage_stats.{}"
	CPU_STATS_TMPL = "docker.cpu_stats.cpu_usage.{}"
	THROTTLING_DATA_TMPL = "docker.cpu_stats.throttling_data.{}"
	PRECPU_STATS_CPU_USAGE_TMPL = "docker.precpu_stats.cpu_usage.{}"
	PRECPU_STATS_THROTTLING_DATA_TMPL = "docker.precpu_stats.throttling_data.{}"
	MEMORY_STATS_TMPL = "docker.memory_stats.{}"
	CONTAINER_RUN_TMPL = "docker.containers.running"
	NUM_PROCESS_TMPL = "docker.num_proces"
#Tags
	WINDOWS_TAG = "os:windows"	
	DOCKER_WIN_TAG = "sources:docker_win"
#Other
	DOCKER_LIST_ALL_CONT = "/containers/json"
	DOCKER_CONTAINER = "/containers/"
	DOCKER_STATS = "/stats"
	DOCKER_IMAGE_KEY = "docker_image:"
	DOCKER_STATE_KEY = "state:"
	DOCKER_STATUS_KEY = "status:"
	DOCKER_CONTAINER_NAME_KEY = "container_name:"
	DOCKER_CONTAINER_ID_KEY = "container_id:"
	DOCKER_GUID_KEY = "guid:"
	DOCKER_TYPE = "docker"
#Docker Metric Mapping
	DOCKER_NETWORK = "networks"
	DOCKER_NETWORK_RX_BYTES = "rx_bytes"
	DOCKER_NETWORK_RX_PACKETS = "rx_packets" 
	DOCKER_NETWORK_RX_ERRORS = "rx_errors" 
	DOCKER_NETWORK_RX_DROPPED = "rx_dropped" 
	DOCKER_NETWORK_TX_BYTES = "tx_bytes"
	DOCKER_NETWORK_TX_PACKETS = "tx_packets" 
	DOCKER_NETWORK_TX_ERRORS = "tx_errors" 
	DOCKER_NETWORK_TX_DROPPED = "tx_dropped"
	DOCKER_MEMORY_STATS= "memory_stats"
	DOCKER_MEMORY_COMMIBYTES = "commitbytes"
	DOCKER_MEMORY_COMMITPEAKBYTES = "commitpeakbytes" 
	DOCKER_MEMORY_PRIATEWORKINGSET = "privateworkingset"
	DOCKER_PRECPU_STATS = "precpu_stats"
	DOCKER_THROTTLING_DATA = "throttling_data"
	DOCKER_THROTTLING_DATA_PERIODS = "periods"
	DOCKER_THROTTLING_DATA_THROTTLED_PERIODS = "throttled_periods"
	DOCKER_THROTTLING_DATA_THROTTLED_TIME = "throttled_time"
	DOCKER_CPU_USAGE = "cpu_usage"
	DOCKER_CPU_USAGE_TOTAL_USAGE = "total_usage"
	DOCKER_CPU_USAGE_USAGE_IN_KERNELMODE = "usage_in_kernelmode"
	DOCKER_CPU_USAGE_USAGE_IN_USERMODE = "usage_in_usermode"
	DOCKER_CPU_STATS = "cpu_stats"
	DOCKER_STORAGE_STATS ="storage_stats"
	DOCKER_STORAGE_STATS_READ_COUNT_NORMALIZED = "read_count_normalized"
	DOCKER_STORAGE_STATS_READ_SIZE_BYTES = "read_size_bytes"
	DOCKER_STORAGE_STATS_READ_WRITE_COUNT_NORMALIZED = "write_count_normalized"
	DOCKER_STORAGE_STATS_READ_WRITE_SIZE_BYTES = "write_size_bytes"
	DOCKER_BLKIO_STATS = "blkio_stats"
	DOCKER_BLKIO_STATS_IO_SERVICE_BYTES_RECURSIVE = "io_service_bytes_recursive"
	DOCKER_BLKIO_STATS_IO_SERVICE_RECURSIVE = "io_serviced_recursive"
	DOCKER_BLKIO_STATS_IO_QUEUE_RECURSIVE = "io_queue_recursive"
	DOCKER_BLKIO_STATS_IO_SERVICE_TIME_RECURSIVE = "io_service_time_recursive"
	DOCKER_BLKIO_STATS_IO_WAIT_TIME_RECURSIVE = "io_wait_time_recursive"
	DOCKER_BLKIO_STATS_IO_MERGED_RECURSIVE = "io_merged_recursive"
	DOCKER_BLKIO_STATS_IO_TIME_RECURSIVE = "io_time_recursive"
	DOCKER_BLKIO_STATS_SECTORS_RECURSIVE = "sectors_recursive"
	DOCKER_NUM_PROCS = "num_procs"

class WindowsDockerCheck(AgentCheck, DockerConstant):
	def _generate_instance_key(self, instance):
		return instance.get('url')

	def _generate_request_session(self, instance):
		sess = requests.Session()
		if instance.get("tls_client_cert"):
			sess.cert = instance.get("tls_client_cert")
		if instance.get("tls_cacert"):
			sess.verify = instance.get("tls_cacert")
		elif instance.get("tls_verify"):
			sess.verify = True
		return sess

	def check(self, instance):
		container_full_ids = []
		container_ids = []
		container_urls = []
		image_lookup = {}

		url = self._generate_instance_key(instance)
		list_all_containers_url=url+self.DOCKER_LIST_ALL_CONT

		session = self._generate_request_session(instance)
		images_json = session.get(url+"/images/json", timeout=1).json()

		for image_def in images_json:
			_, image_id = image_def.get("Id").split(":", 1)
			repo_tags = image_def.get("RepoTags", [])
			image_lookup[image_id] = repo_tags

		containers_response = session.get(list_all_containers_url, timeout=1).json()
		container_count = len(containers_response)

		for container in containers_response:
			container_full_ids.append(container["Id"])
			_, image_hash = container["ImageID"].split(":", 1)
			raw_image_tags = image_lookup.get(image_hash, [image_hash])

			id_tag = self.DOCKER_WIN_TAG
			image_tags = [self.DOCKER_IMAGE_KEY + tag for tag in raw_image_tags]
			state_tag = self.DOCKER_STATE_KEY + container["State"].lower()
			status_tag = self.DOCKER_STATUS_KEY + container["Status"].lower()
			name_tag = self.DOCKER_CONTAINER_NAME_KEY + container["Names"][0].lower()

			self.event({
				"event_type": self.DOCKER_TYPE,
				"msg_title": 'Could use review from team.',
				"alert_type": 'info',
				"source_type_name": self.DOCKER_TYPE,
				"tags": [self.DOCKER_WIN_TAG] + image_tags,
				"msg_text": "Docker"
			})

	# running containers:
		self.gauge(self.CONTAINER_RUN_TMPL, container_count, tags=[self.WINDOWS_TAG])

		for x in container_full_ids:
			container_urls.append(url+self.DOCKER_CONTAINER+x+self.DOCKER_STATS)
			container_ids.append(x[:12])

		for index, value in enumerate(container_urls):
			cont_health_response = session.get(value, stream=True)
			for raw_stream in cont_health_response.iter_lines():
				short_container_id = self.DOCKER_CONTAINER_ID_KEY+container_ids[index]
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
					self.gauge('docker.read_at',d,tags=[short_container_id,self.WINDOWS_TAG])

				#num_proces:
					num_procs=rs[self.DOCKER_NUM_PROCS]
					self.gauge(self.NUM_PROCESS_TMPL, num_procs, tags=[short_container_id,self.WINDOWS_TAG])

				#blkio_stats:
					blkio_stats=rs[self.DOCKER_BLKIO_STATS]
					for blkio_stats_prop in [self.DOCKER_BLKIO_STATS_IO_SERVICE_BYTES_RECURSIVE,self.DOCKER_BLKIO_STATS_IO_SERVICE_RECURSIVE,self.DOCKER_BLKIO_STATS_IO_QUEUE_RECURSIVE,self.DOCKER_BLKIO_STATS_IO_SERVICE_TIME_RECURSIVE,self.DOCKER_BLKIO_STATS_IO_WAIT_TIME_RECURSIVE,self.DOCKER_BLKIO_STATS_IO_MERGED_RECURSIVE,self.DOCKER_BLKIO_STATS_IO_TIME_RECURSIVE,self.DOCKER_BLKIO_STATS_SECTORS_RECURSIVE]:
						self.gauge(self.BLKIO_STATS_TMPL.format(blkio_stats_prop), blkio_stats[blkio_stats_prop], tags=[short_container_id,self.WINDOWS_TAG])

				#storage_stats:
					storage_stats=rs[self.DOCKER_STORAGE_STATS]
					for storage_stats_prop in [self.DOCKER_STORAGE_STATS_READ_COUNT_NORMALIZED,self.DOCKER_STORAGE_STATS_READ_SIZE_BYTES,self.DOCKER_STORAGE_STATS_READ_WRITE_COUNT_NORMALIZED,self.DOCKER_STORAGE_STATS_READ_WRITE_SIZE_BYTES]:
						self.gauge(self.STORAGE_STATS_TMPL.format(storage_stats_prop), storage_stats[storage_stats_prop], tags=[short_container_id,self.WINDOWS_TAG])

				#cpu_stats:
					cpu_usage=rs[self.DOCKER_CPU_STATS][self.DOCKER_CPU_USAGE]
					for cpu_stat_prop in [self.DOCKER_CPU_USAGE_TOTAL_USAGE,self.DOCKER_CPU_USAGE_USAGE_IN_KERNELMODE,self.DOCKER_CPU_USAGE_USAGE_IN_USERMODE]:
						self.gauge(self.CPU_STATS_TMPL.format(cpu_stat_prop), cpu_usage[cpu_stat_prop], tags=[short_container_id,self.WINDOWS_TAG])

					throttling_data=rs[self.DOCKER_CPU_STATS][self.DOCKER_THROTTLING_DATA]
					for throttling_data_prop in [self.DOCKER_THROTTLING_DATA_PERIODS,self.DOCKER_THROTTLING_DATA_THROTTLED_PERIODS,self.DOCKER_THROTTLING_DATA_THROTTLED_TIME]:
						self.gauge(self.THROTTLING_DATA_TMPL.format(throttling_data_prop), throttling_data[throttling_data_prop], tags=[short_container_id,self.WINDOWS_TAG])

				#precpu_stats:
					precpu_stats=rs[self.DOCKER_PRECPU_STATS][self.DOCKER_CPU_USAGE]
					for precpu_prop in [self.DOCKER_CPU_USAGE_TOTAL_USAGE,self.DOCKER_CPU_USAGE_USAGE_IN_KERNELMODE,self.DOCKER_CPU_USAGE_USAGE_IN_USERMODE]:
						self.gauge(self.PRECPU_STATS_CPU_USAGE_TMPL.format(precpu_prop), precpu_stats[precpu_prop], tags=[short_container_id,self.WINDOWS_TAG])
					
					precpu_throttling_data=rs[self.DOCKER_PRECPU_STATS][self.DOCKER_THROTTLING_DATA]
					for precpu_throttling_prop in [self.DOCKER_THROTTLING_DATA_PERIODS,self.DOCKER_THROTTLING_DATA_THROTTLED_PERIODS,self.DOCKER_THROTTLING_DATA_THROTTLED_TIME]:
						self.gauge(self.PRECPU_STATS_THROTTLING_DATA_TMPL.format(precpu_throttling_prop), precpu_throttling_data[precpu_throttling_prop], tags=[short_container_id,self.WINDOWS_TAG])

				#memory_stats:
					memory_stats=rs[self.DOCKER_MEMORY_STATS]
					for memory_stat_prop in [self.DOCKER_MEMORY_COMMIBYTES, self.DOCKER_MEMORY_COMMITPEAKBYTES, self.DOCKER_MEMORY_PRIATEWORKINGSET]:
						self.gauge(self.MEMORY_STATS_TMPL.format(memory_stat_prop), memory_stats[memory_stat_prop], tags=[short_container_id,self.WINDOWS_TAG])

				#networks:
					networks=rs[self.DOCKER_NETWORK]
					for guid, data in networks.iteritems():
						guid_tag = self.DOCKER_GUID_KEY+guid
						for prop in [self.DOCKER_NETWORK_RX_BYTES,self.DOCKER_NETWORK_RX_PACKETS,self.DOCKER_NETWORK_RX_ERRORS,self.DOCKER_NETWORK_RX_DROPPED,self.DOCKER_NETWORK_TX_BYTES,self.DOCKER_NETWORK_TX_PACKETS,self.DOCKER_NETWORK_TX_ERRORS,self.DOCKER_NETWORK_TX_DROPPED]:
							self.gauge(self.NET_TMPL.format(prop), data[prop], tags=[short_container_id, guid_tag,self.WINDOWS_TAG])

				break