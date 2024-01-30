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
        self.v1compat = self.instance.get('v1compat', True)
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

    def _list_projects(self) -> List[str]:
        """
        List all projects in the organization.

        Returns:
        List[str]: A list of project names.
        """
        endpoint = f'v2/list-projects/{self.organization}'
        response = self._call(endpoint)

        if response.status_code != 200:
            self.log.info('Failed to GET projects. Status Code : %s', {response.status_code})
            return []

        # Extract project names
        project_names = [project["name"] for project in response.json()["data"]["projects"]]

        # Output the project names
        return project_names

    def _list_models(self, project: str) -> List[str]:
        """
        List all models in a project.

        Parameters:
        project (str): The name of the project.

        Returns:
        List[str]: A list of model names.
        """
        endpoint = f'v2/models?organization_name={self.organization}&project_name={project}'
        response = self._call(endpoint)

        if response.status_code != 200:
            self.log.info('Failed to GET models. Status Code : %s', {response.status_code})
            return []

        # Extract model names
        model_names = [item["name"] for item in response.json()["data"]["items"]]

        return model_names

    def _get_metrics(self, project: str, model: str) -> (list, list):
        """
        Retrieve metrics for a specific model.

        Parameters:
        project (str): The name of the project.
        model (str): The name of the model.

        Returns:
        list: The metrics data for the specified model.
        list: The outputs for the specified model.

        """
        endpoint = f'v2/metrics/{self.organization}:{project}:{model}'
        response = self._call(endpoint)
        if response.status_code != 200:
            self.log.info('Failed to GET metrics query. Status Code : %s', {response.status_code})
            return [], []

        self.log.debug('METRICS Response : %s', response.json())

        outputs = []
        for column in response.json()['data']['columns']:
            if column.get('group', '') == 'Outputs':
                outputs.append(column['key'])

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
        self, project: str, model: str, result: Dict[str, Any], outputs: list
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

        metric_type = result['metric_type']
        metric = result.get('metric')
        value_list = result['data'][-1] if result['data'] else 0
        gauge_results = []

        # Update metric names if necessary
        metric_mapping = {'traffic': 'traffic_count', 'jsd': 'histogram_drift'}
        metric = metric_mapping.get(metric, metric)

        for col_idx, col_name in enumerate(result['col_names']):
            if col_name == 'timestamp':
                continue

            col_name_list = col_name.split(',')

            # Determine the column name based on metric type and structure
            if metric_type == 'data_integrity' and len(col_name_list) == 2:
                col_name = f'{col_name_list[1]}/{col_name_list[0]}'
            elif len(col_name_list) >= 2:
                col_name = col_name_list[1]

            # Create appropriate tags
            tags = self._create_tags(project, model, col_name if metric_type != 'performance' else None)

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

            tags = self._create_tags(project, model, col_name)
            gauge_results.append((metric, value_list[col_idx], tags))

        return gauge_results

    def _run_queries(self, project: str, model: str) -> (Dict[str, Any], list):
        """
        Run queries for a given model within a specified time range.

        Parameters:
        project (str): The project name.
        model (str): The model object containing details like organization_name, project_name, and name.
        bin_size (int): The size of the time bin in seconds for the query.

        Returns:
        Dict[str, Any]: The JSON response from the query execution.
        """

        start_time_epoch = (time.time() * 1000) - (self.bin_size * 1000) - (self.delay * 1000)
        end_time_epoch = time.time() * 1000 - (self.delay * 1000)

        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time_epoch / 1000))
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(end_time_epoch / 1000))

        bin_size_str = 'Five_Minute'
        if self.bin_size == 3600:
            bin_size_str = 'Hour'
        elif self.bin_size == 86400:
            bin_size_str = 'Day'
        elif self.bin_size == 604800:
            bin_size_str = 'Week'
        elif self.bin_size == 2592000:
            bin_size_str = 'Month'

        metrics, outputs = self._get_metrics(project, model)
        if len(metrics) == 0:
            return {}, []

        queries = []
        for metric in metrics:
            metric_type = metric['type']
            if metric_type not in self.enabled_metrics:
                continue

            if metric.get('needs_categories', False):
                continue

            queries.append(
                {
                    'query_key': metric['key'],
                    'categories': [],
                    'columns': metric['columns'],
                    'viz_type': 'line',
                    'metric': metric['key'],
                    'metric_type': metric['type'],
                    'model_name': model,
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
            'organization_name': self.organization,
            'project_name': project,
            'query_type': 'MONITORING',
            'queries': queries,
        }
        self.log.info('Running query for Project:%s Model:%s', project, model)
        result = self._call('v2/queries', json_request)
        if result.status_code != 200:
            self.log.info(
                'Failed to run query for Project:%s Model:%s Status Code : %s', project, model, result.status_code
            )
            return {}, []

        self.log.debug('Query request : %s', json_request)
        self.log.debug('Query result : %s', result.json())

        return result.json(), outputs

    def _parse_query_results(self, query_results: Dict[str, Any], outputs: list) -> List[Tuple[str, Any, List[str]]]:
        """
        Parse the results from query execution and convert them to a compatible format.

        Parameters:
        query_results (Dict[str, Any]): The results from the query execution.

        Returns:
        List[Tuple[str, Any, List[str]]]: A list of tuples with metric data.
        """

        all_gauge_results = []
        if len(query_results) == 0:
            return []

        for result in query_results['data']['results']:
            for v in result.values():
                if self.v1compat:
                    all_gauge_results.extend(
                        self._process_v1compat_query_result(
                            query_results['data']['project_name'], v['model_name'], v, outputs
                        )
                    )
                else:
                    all_gauge_results.extend(
                        self._process_query_result(query_results['data']['project_name'], v['model_name'], v)
                    )

        self.log.info('Parsed query results : %s', all_gauge_results)

        return all_gauge_results

    def _run(self):
        """
        Run the check and collect metrics from all projects and models.
        """
        all_gauge_results = []
        for project in self._list_projects():
            for model in self._list_models(project):
                try:
                    self.log.info('Running check for Project:%s Model:%s', project, model)
                    query_results, outputs = self._run_queries(project, model)
                    if query_results:
                        all_gauge_results.extend(self._parse_query_results(query_results, outputs))
                except Exception as e:
                    self.log.error('FiddlerCheck encountered an error: %s', e)

        self.log.info('FiddlerCheck run complete: %s', len(all_gauge_results))
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
