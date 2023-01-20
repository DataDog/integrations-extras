import time

import fiddler as fdl

from datadog_checks.base import AgentCheck

metrics_list = ['accuracy', 'traffic_count', 'histogram_drift', 'feature_average', 'output_average']


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

        print("Here is what is passed in to check.py's constructor...")
        print(f"name: {name}")
        print(f"init_config: {init_config}")
        print(f"instances: {instances}")

        self.base_url = self.instance.get('url')
        self.api_key = self.instance.get('fiddler_api_key')
        self.org = self.instance.get('organization')
        # Set the Fiddler bin size to the same number of seconds as the check runs.
        # Thus if the check runs every 5 mins, make the bin_size for fiddler 5 minutes (aka. 300 secs)
        # self.bin_size = int(self.instance.get('minimum_collection_interval'))
        self.bin_size = 300  # aka 5 mins

        self.log.info("Connecting to : %s", self.base_url)
        print("Connecting to: " + str(self.base_url))
        print("Org: " + str(self.org))
        print("Auth: " + str(self.api_key))

        self.client = None

    def check(self, _):
        if not self.client:
            self.client = fdl.FiddlerApi(url=self.base_url, org_id=self.org, auth_token=self.api_key)

        # Iterate through the projects and the models and push data into Fiddler
        print('\n\n ------------------ New Check -----------------------------')
        project_path = ['list_projects', self.org]
        result_all = self.client.v1._call(project_path)

        TEN_MINUTE_DELAY = 10 * 60 * 1000
        start_time_epoch = (time.time() * 1000) - (self.bin_size * 1000) - TEN_MINUTE_DELAY
        end_time_epoch = time.time() * 1000 - TEN_MINUTE_DELAY
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time_epoch / 1000))
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(end_time_epoch / 1000))

        print(f"start time epoch: {start_time_epoch}")
        print(f"end time epoch: {end_time_epoch}")
        print(f"Start time is : {start_time}")
        print(f"End time is : {end_time}")

        # Iterate through all of the projects within the Fiddler instance and get the metrics
        for project in result_all["projects"]:
            models = project["models"]

            # Iterate through all of the models within a project
            for model in models:
                print("Model: %s" % model["id"])

                # Do the above iteration for every metric that we need publish.
                for metric in metrics_list:
                    print("Metric is : %s" % metric)
                    json_request = {
                        "metric": metric,
                        "time_range_start": start_time_epoch,
                        "time_range_end": end_time_epoch,
                        "bin_size": self.bin_size,
                    }
                    agg_metrics_path = ['aggregated_metrics', self.org, project["name"], model["id"]]
                    print("Project and Model and metric: %s %s %s" % (project["name"], model["id"], metric))

                    hit_exception = False
                    try:
                        result = self.client.v1._call(agg_metrics_path, json_request)
                    except Exception:
                        print("Aggregated metrics exception : %s" % (agg_metrics_path))
                        print("Project with no monitoring data. ProjectModel: %s %s %s" %
                              (project["name"], model["id"], metric))
                        hit_exception = True

                    if hit_exception:
                        print("Hit the exception.")
                        hit_exception = False
                        continue

                    # iterate through the json result for that specific metric
                    for single_value in result["values"]:
                        start_time = int(time.time()) * 1000

                        # Every metric has a different way of providing the value. So handle them separetly.
                        if metric == 'traffic_count':
                            value = single_value["value"]
                            print("traffic Final list: %s %s %s %s %s" %
                                  (project["name"], model["id"], start_time, metric, value))
                            tags = create_tags(project=project["name"], model=model["id"])
                            self.gauge(metric, value, tags)

                        elif metric == 'output_average' or metric == 'integrity_violation_count':
                            for key, value in single_value["value"].items():
                                # new_metric = metric + '-' + key
                                new_metric = metric
                                print("output_average Final list: %s %s %s %s %s" %
                                      (project["name"], model["id"], start_time, new_metric, value))
                                tags = create_tags(project=project["name"], model=model["id"], feature=key)
                                self.gauge(new_metric, value, tags)

                        elif metric == 'histogram_drift':
                            for key, value in single_value["value"].items():
                                # new_metric = "histogram_drift-" + key
                                new_metric = metric
                                print("hist Final list: %s %s %s %s %s" %
                                      (project["name"], model["id"], start_time, new_metric, value))
                                tags = create_tags(project=project["name"], model=model["id"], feature=key)
                                self.gauge(new_metric, value, tags)

                        elif metric == 'feature_average':
                            for key, value in single_value["value"].items():
                                new_metric = metric
                                print("feature_average Final list: %s %s %s %s %s" %
                                      (project["name"], model["id"], start_time, new_metric, value))
                                tags = create_tags(project=project["name"], model=model["id"], feature=key)
                                self.gauge(new_metric, value, tags)

                        elif metric == 'accuracy':
                            accuracy_metrics = single_value["value"]
                            for key, value in accuracy_metrics["accuracy_metrics"].items():
                                new_metric = key
                                print("accuracy Final list: %s %s %s %s %s" %
                                      (project["name"], model["id"], start_time, new_metric, value))
                                tags = create_tags(project=project["name"], model=model["id"])
                                self.gauge(new_metric, value, tags)

        # If the check ran successfully, we can send the status.
        # More info at
        # https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck.service_check

        self.service_check("can_connect", AgentCheck.OK)
