from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.base.checks.openmetrics.v2.transform import NATIVE_TRANSFORMERS

from .config_models import ConfigMixin
from .metrics import METRIC_MAP

GLOBAL_DB_NAME = 'global'


class Neo4jCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = 'neo4j'

    def __init__(self, name, init_config, instances):
        super().__init__(name, init_config, instances)

        self.check_initializations.append(self.configure_additional_transformers)

    def configure_transformer(self, metric_name):
        cached_metric_data = {}

        def custom_transformer(metric, sample_data, runtime_data):
            if metric.name in cached_metric_data:
                data = cached_metric_data[metric.name]
                if data is None:
                    return

                transformer, db_tag = data
            else:
                if metric.name.startswith('neo4j_dbms_'):
                    db_name = GLOBAL_DB_NAME
                    final_metric_name = metric_name
                elif metric.name.startswith('neo4j_database_'):
                    db_name, _, final_metric_name = metric.name.replace('neo4j_database_', '', 1).partition('_')
                    if self.config.neo4j_dbs and db_name not in self.config.neo4j_dbs:
                        cached_metric_data[metric.name] = None
                        return
                elif metric.name.startswith('neo4j_transaction_'):
                    db_name, _, final_metric_name = metric.name.replace('neo4j_transaction_', '', 1).partition('_')
                    if self.config.neo4j_dbs and db_name not in self.config.neo4j_dbs:
                        cached_metric_data[metric.name] = None
                        return
                else:
                    db_name = GLOBAL_DB_NAME
                    final_metric_name = metric_name
                    if self.config.neo4j_dbs and self.config.neo4j_version.startswith('5.'):
                        if metric.name.startswith('neo4j_'):
                            raw_metric_name = metric.name.replace('neo4j_', '', 1)
                        else:
                            raw_metric_name = metric.name

                        for db in self.config.neo4j_dbs:
                            prefix = f'{db}_'
                            if raw_metric_name.startswith(prefix):
                                db_name = db
                                break

                db_tag = f'db_name:{db_name}'
                transformer = NATIVE_TRANSFORMERS[metric.type](self, final_metric_name, {}, {})
                cached_metric_data[metric.name] = (transformer, db_tag)

            new_sample_data = []
            for sample, tags, hostname in sample_data:
                tags.append(db_tag)
                new_sample_data.append((sample, tags, hostname))

            transformer(metric, new_sample_data, runtime_data)

        return custom_transformer

    def configure_additional_transformers(self):
        metric_transformer = self.scrapers[self.config.openmetrics_endpoint].metric_transformer

        for raw_metric_name, metric_name in METRIC_MAP.items():
            metric_transformer.add_custom_transformer(
                f'.*?{raw_metric_name}$', self.configure_transformer(metric_name), pattern=True
            )
