import json
import requests
from datadog_checks.base import AgentCheck, ConfigurationError

APIURL = 'https://api.appkeeper.sios.com/v2/'

class AppKeeperCheck(AgentCheck):
    def check(self, instance):
        account = instance.get('account')
        integrationToken = instance.get('integrationToken')

        if not account or not integrationToken:
            raise ConfigurationError('Configuration error, please fix conf.yaml')

        # APIキーの取得
        # response = requests.get(APIURL + 'authorize?token=' + integrationToken)
        # TODO エラーの場合の処理
        # apiKey = json.loads(response.text)
        self.log.info('hoge')
        self.gauge('appkeeper.api_recover_count', 0)
        self.gauge('appkeeper.integrated_instances', 1)
        self.gauge('appkeeper.all_instances', 3)
