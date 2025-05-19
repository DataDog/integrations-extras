import time
from typing import Any, Dict, List, Optional, Tuple

import requests

from datadog_checks.base import AgentCheck


class FiddlerCheck(AgentCheck):
    """
    An integration check for Fiddler, collecting and submitting metrics to Datadog.
    """

    __NAMESPACE__ = 'fiddler'

    def __init__(self, name, init_config, instances):
        super().__init__(name, init_config, instances)

        # Configuration parameters
        self.url = self.instance.get('url')
        self.organization = self.instance.get('organization')
        self.token = self.instance.get('fiddler_api_key')
        self.timeout = self.instance.get('timeout', 300)
        self.v1compat = self.instance.get('v1compat', False)
        self.enabled_metrics = self.instance.get(
            'enabled_metrics', ['drift', 'traffic', 'performance', 'statistic', 'service_metrics']
        )
        self.bin_size = self.instance.get('bin_size', 3600)
        self.delay = self.instance.get('delay', 0)  # delay in seconds

        self.log.info('Fiddler URL: %s', self.url)

    def _call(self, endpoint: str, json_request: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Make an API call to the Fiddler server.

        :param endpoint: The API endpoint to be accessed.
        :param json_request: The JSON payload for POST requests.
        :return: The response from the Fiddler server.
        """
        headers = {
            'Authorization': f'Bearer {self.token}',
            'X-Integration': 'fiddler-datadog',
        }

        full_url = f'{self.url}/{endpoint}'

        try:
            if json_request:
                response = requests.post(full_url, headers=headers, json=json_request, timeout=self.timeout)
            else:
                response = requests.get(full_url, headers=headers, timeout=self.timeout)
        except Exception as e:
            self.log.error('Error during HTTP request to %s: %s', full_url, e)
            return None

        return response

    def _list_models(self) -> List[str]:
        """
        List all models in the organization.

        Returns:
        List[str]: A list of model identifiers.
        """
        endpoint = 'v3/models'
        response = self._call(endpoint)

        if response.status_code != 200:
            self.log.info('Failed to GET models. Status Code : %s', {response.status_code})
            return []

        # Extract model compact
        model_compact = [
            {'id': item['id'], 'name': item['name'], 'project': item['project']}
            for item in response.json()['data']['items']
        ]

        return model_compact

    def _get_baseline_id(self, model_id: str, baseline_name: str) -> str:
        """
        Get the baseline id for a specific model.

        Parameters:
        model_id (str): The model identifier.
        baseline_name (str): The baseline name.

        Returns:
        str: The baseline id for the specified model.
        """
        endpoint = f"v3/models/{model_id}/baselines"
        response = self._call(endpoint)
        if response.status_code != 200:
            self.log.info('Failed to GET baselines query. Status Code : %s', {response.status_code})
            return ""

        self.log.info('BASELINE Response : %s', response.json())

        for baseline in response.json()['data']['items']:
            if baseline['name'] == baseline_name:
                return baseline['id']
        if response.json()['data']['items']:
            return response.json()['data']['items'][0]['id']
        return ""

    def _get_metrics(self, model: dict) -> tuple[list, list]:
        """
        Retrieve metrics for a specific model.

        Parameters:
        model (dict): Model identifier dict containing the model name and id.

        Returns:
        list: The metrics data for the specified model.
        list: The outputs for the specified model.

        """
        endpoint = f"v3/models/{model['id']}/metrics"
        response = self._call(endpoint)
        if response.status_code != 200:
            self.log.info('Failed to GET metrics query. Status Code : %s', {response.status_code})
            return [], []

        self.log.info('METRICS Response : %s', response.json())

        outputs = []
        for column in response.json()['data']['columns']:
            if column.get('group', '') == 'Outputs':
                outputs.append(column['id'])

        return response.json()['data']['metrics'], outputs

    def _create_tags(self, project: str, model: str, feature: Optional[str] = None) -> List[str]:
        """
        Create tags for identifying metrics.

        Parameters:
        project (str): The project name.
        model (str): The model name.
        feature (Optional[str]): The feature name.

        Returns:
        List[str]: A list of tags for the metric.
        """
        tags = []
        if project:
            tags.append('project:' + project)

        if model:
            tags.append('model:' + model)

        if feature:
            tags.append('feature:' + feature)
        return tags

    def _process_v1compat_query_result(
        self, project_name: str, model_name: str, result: Dict[str, Any], outputs: list
    ) -> List[Tuple[str, Any, List[str]]]:
        """
        Convert metrics to a format compatible with v1 and v2.

        Parameters:
        project (str): The project name.
        model (str): The model name.
        result (Dict[str, Any]): The metrics data.

        Returns:
        List[Tuple[str, Any, List[str]]]: Processed metrics in a compatible format.
        """

        metric = result.get('metric')
        value_list = result['data'][-1] if result['data'] else 0
        gauge_results = []

        # mapping to old metric names for backward compatibility
        metric_mapping = {
            'traffic': 'traffic_count',
            'jsd': 'histogram_drift',
            'expected_calibration_error': 'expected_callibration_error',
            'calibrated_threshold': 'callibrated_threshold',
            'geometric_mean': 'g_mean',
            'log_loss': 'binary_cross_entropy',
            'recall': 'tpr',
            'ndcg_mean': 'mean_ndcg',
        }
        metric = metric_mapping.get(metric, metric)

        di_metric_mapping = {
            'null_violation_count': 'is_null_violation',
            'range_violation_count': 'is_range_violation',
            'type_violation_count': 'is_type_violation',
            'any_violation_count': '__ANY__',
        }

        for col_idx, col_name in enumerate(result['col_names']):
            if col_name == 'timestamp':
                continue

            col_name_list = col_name.split(',')

            # Determine the column name based on metric type and structure
            if metric in di_metric_mapping and len(col_name_list) == 2:
                fixed_metric_name = di_metric_mapping.get(col_name_list[0], col_name_list[0])
                col_name = f'{col_name_list[1]}/{fixed_metric_name}'
            elif len(col_name_list) >= 2:
                col_name = col_name_list[1]
            elif len(col_name_list) == 1:
                col_name = None

            # Create appropriate tags
            tags = self._create_tags(project_name, model_name, col_name)

            # Determine the metric name and append to results
            if metric == 'average':
                metric_name = 'output_average' if col_name in outputs else 'feature_average'
                gauge_results.append((metric_name, value_list[col_idx], tags))
            else:
                gauge_results.append((metric, value_list[col_idx], tags))

        return gauge_results

    def _process_query_result(
        self, project: str, model: str, result: Dict[str, Any]
    ) -> List[Tuple[str, Any, List[str]]]:
        """
        Process metrics data without v1v2 compatibility.

        Parameters:
        project (str): The project name.
        model (str): The model name.
        result (Dict[str, Any]): The metrics data.

        Returns:
        List[Tuple[str, Any, List[str]]]: Processed metrics.
        """
        metric = result['metric']
        value_list = result['data'][-1] if len(result['data']) > 0 else 0
        gauge_results = []

        col_idx = -1
        for col_name in result['col_names']:
            col_idx += 1

            # skip timestamp
            if col_name == 'timestamp':
                continue
            col_name_list = col_name.split(',')
            if len(col_name_list) == 1:
                col_name = None
            tags = self._create_tags(project, model, col_name)
            gauge_results.append((metric, value_list[col_idx], tags))

        return gauge_results

    def _run_queries(self, model: dict) -> tuple[dict[str, Any], list]:
        """
        Run queries for a given model within a specified time range.

        Parameters:
        model (dict): The model identifier dict containing the model name and id.

        Returns:
        Dict[str, Any]: The JSON response from the query execution.
        list: The outputs for the specified model.
        """

        start_time_epoch = (time.time() * 1000) - (self.bin_size * 1000) - (self.delay * 1000)
        end_time_epoch = time.time() * 1000 - (self.delay * 1000)

        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time_epoch / 1000))
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(end_time_epoch / 1000))
        model_name = model.get('name')
        model_id = model.get('id')
        project_name = model.get('project', {}).get('name')
        project_id = model.get('project', {}).get('id')

        bin_size_str = 'Five_Minute'
        if self.bin_size == 3600:
            bin_size_str = 'Hour'
        elif self.bin_size == 86400:
            bin_size_str = 'Day'
        elif self.bin_size == 604800:
            bin_size_str = 'Week'
        elif self.bin_size == 2592000:
            bin_size_str = 'Month'

        metrics, outputs = self._get_metrics(model)
        if len(metrics) == 0:
            return {}, []

        queries = []
        default_baseline_name = "default_static_baseline"
        baseline_id = ""
        for metric in metrics:
            metric_type = metric['type']
            if metric_type not in self.enabled_metrics:
                continue

            if metric.get('requires_categories', False):
                continue

            if metric.get('requires_baseline', False):
                baseline_id = self._get_baseline_id(model_id, default_baseline_name)
                if not baseline_id:
                    continue

            queries.append(
                {
                    'query_key': metric.get('id'),
                    'categories': [],
                    'columns': metric.get('columns'),
                    'viz_type': 'line',
                    'metric': metric.get('id'),
                    'metric_type': metric.get('type'),
                    'model_id': model_id,
                    'baseline_id': baseline_id,
                }
            )

        json_request = {
            'filters': {
                'bin_size': bin_size_str,
                'time_range': {
                    'start_time': start_time,
                    'end_time': end_time,
                },
                'time_zone': 'UTC',
            },
            'project_id': project_id,
            'query_type': 'MONITORING',
            'queries': queries,
        }

        self.log.info('Running query for Project: %s Model: %s', project_name, model_name)
        self.log.info('Query request : %s', json_request)
        resp = self._call('v3/queries', json_request)
        if resp.status_code != 200:
            self.log.info(
                'Failed to run query for Project: %s Model: %s Status Code : %s',
                project_name,
                model_name,
                resp.status_code,
            )
            return {}, []

        self.log.info('Query request : %s', json_request)

        return resp.json(), outputs

    def _parse_query_results(self, query_results: Dict[str, Any], outputs: list) -> List[Tuple[str, Any, List[str]]]:
        """
        Parse the results from query execution and convert them to a compatible format.

        Parameters:
        query_results (Dict[str, Any]): The results from the query execution.

        Returns:
        List[Tuple[str, Any, List[str]]]: A list of tuples with metric data.
        """

        all_gauge_results = []
        results = query_results.get('data', {}).get('results', {})
        if not query_results['data']['results']:
            return []
        self.log.info('Query results : %s', results)
        for v in results.values():
            if self.v1compat:
                all_gauge_results.extend(
                    self._process_v1compat_query_result(
                        project_name=query_results['data']['project']['name'],
                        model_name=v['model']['name'],
                        result=v,
                        outputs=outputs,
                    )
                )
            else:
                all_gauge_results.extend(
                    self._process_query_result(query_results['data']['project']['name'], v['model']['name'], v)
                )

        self.log.info('Parsed query results : %s', all_gauge_results)

        return all_gauge_results

    def _run(self):
        """
        Run the check and collect metrics from all models.
        """
        all_gauge_results = []
        for model in self._list_models():
            try:
                self.log.info('Running check for  Model: %s', model['name'])
                query_results, outputs = self._run_queries(model)
                if query_results:
                    all_gauge_results.extend(self._parse_query_results(query_results, outputs))
            except Exception as e:
                self.log.error('FiddlerCheck encountered an error: %s', e)

        self.log.info('FiddlerCheck run complete: %s', len(all_gauge_results))
        self.log.info('FiddlerCheck results: %s', all_gauge_results)
        return all_gauge_results

    def check(self, _):
        """
        Main entry point for the check.
        """
        # Run the check
        check_results = self._run()

        print(check_results)

        # Submit the metrics
        for metric_name, metric_value, tags in check_results:
            self.gauge(metric_name, metric_value, tags=tags)

        # Send service check status
        self.service_check("can_connect", AgentCheck.OK)
