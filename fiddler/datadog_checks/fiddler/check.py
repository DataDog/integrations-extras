import time

import fiddler as fdl

from datadog_checks.base import AgentCheck

# We will get one hours worth data in chunks and process them.
bin_size = 3600

metrics_list = ['accuracy']


def create_tags(**tags_in):
    tags = []

    tags.append("project:" + tags_in['project'])
    tags.append("model:" + tags_in['model'])
    if len(tags_in) > 2:
        tags.append("feature:" + tags_in['feature'])

    return tags


class FiddlerCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'fiddler'

    def __init__(self, name, init_config, instances):
        super(FiddlerCheck, self).__init__(name, init_config, instances)

        self.base_url = self.instance.get('url')
        self.api_key = self.instance.get('fiddler_api_key')
        self.org = self.instance.get('organization')

        self.log.info("Connecting to : ", self.base_url)
        self.log.info("with org id : ", self.org)
        self.log.info("and auth key : ", self.api_key)

        self.client = fdl.FiddlerApi(url=self.base_url, org_id=self.org, auth_token=self.api_key)

    # Use self.instance to read the check configuration

    def check(self, _):
        # Iterate through the projects and the models and push data into Fiddler
        project_path = ['list_projects', self.org]
        result_all = self.client.v1._call(project_path)

        start_time = (time.time() * 1000) - (bin_size * 1000)
        end_time = time.time() * 1000
        self.log.debug("Start time is : ", start_time)
        self.log.debug("End time is : ", end_time)

        # Iterate through all of the projects within the Fiddler instance and get the metrics
        for project in result_all["projects"]:
            models = project["models"]

            # Iterate through all of the models within a project
            for model in models:
                self.log.debug("Model: ", model["id"])
                for metric in metrics_list:
                    self.log.debug("Metric is :", metric)
                    json_request = {
                        "metric": metric,
                        "time_range_start": start_time,
                        "time_range_end": end_time,
                        "bin_size": bin_size,
                        "prediction": '_',
                    }
                    agg_metrics_path = ['aggregated_metrics', self.org, project["name"], model["id"]]
                    self.log.debug("ProjectModel: ", project["name"], model["id"], metric)
                    # result = self.client._call(agg_metrics_path, json_request)

                    hit_exception = False
                    try:
                        result = self.client.v1._call(agg_metrics_path, json_request)
                    except Exception:
                        self.log.info("Aggregated metrics exception : ", agg_metrics_path)
                        self.log.info(
                            "Project with no monitoring data. ProjectModel: ", project["name"], model["id"], metric
                        )
                        hit_exception = True

                    if hit_exception:
                        self.log.info("Hit the exception.")
                        hit_exception = False
                        continue

                    self.log.debug("Agg_metrics_path: ", agg_metrics_path)
                    self.log.debug("json request: ", json_request, "\n")
                    self.log.debug("Result : ", result, "\n")

                    # iterate through the json result for that specific metric
                    for single_value in result["values"]:
                        start_time = int(time.time()) * 1000

                        # Every metric has a different way of providing the value. So handle them separetly.
                        if metric == 'traffic_count':
                            value = single_value["value"]
                            self.log.debug("Final list: %s %s %s %s %s", project["name"], model["id"], start_time, metric, value)
                            tags = create_tags(project=project["name"], model=model["id"])
                            self.gauge(metric, value, tags)

                        elif metric == 'output_average' or metric == 'integrity_violation_count':
                            for key, value in single_value["value"].items():
                                new_metric = key
                                value = value
                                self.log.debug(
                                    "Final list: %s %s %s %s %s", project["name"], model["id"], start_time, new_metric, value
                                )
                                tags = create_tags(project=project["name"], model=model["id"])
                                self.gauge(metric, value, tags)

                        elif metric == 'histogram_drift':
                            for key, value in single_value["value"].items():
                                new_metric = "histogram_drift-" + key
                                value = value
                                self.log.debug(
                                    "Final list: %s %s %s %s %s", project["name"], model["id"], start_time, new_metric, value
                                )
                                tags = create_tags(project=project["name"], model=model["id"], feature=key)
                                self.gauge(metric, value, tags)

                        elif metric == 'feature_average':
                            for key, value in single_value["value"].items():
                                new_metric = key
                                value = value
                                self.log.debug(
                                    "Final list: %s %s %s %s %s", project["name"], model["id"], start_time, new_metric, value
                                )
                                tags = create_tags(project=project["name"], model=model["id"], feature=key)
                                self.gauge(metric, value, tags)

                        elif metric == 'accuracy':
                            accuracy_metrics = single_value["value"]
                            for key, value in accuracy_metrics["accuracy_metrics"].items():
                                new_metric = key
                                value = value
                                self.log.debug(
                                    "Final list: %s %s %s %s %s", project["name"], model["id"], start_time, new_metric, value
                                )
                                tags = create_tags(project=project["name"], model=model["id"])
                                self.gauge(metric, value, tags)
        # If the check ran successfully, we can send the status.
        # More info at
        # https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck.service_check

        self.service_check("fiddler.can_connect", AgentCheck.OK)
