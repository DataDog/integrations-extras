from datadog_checks.dev import get_docker_hostname

URL = 'http://{}'.format(get_docker_hostname())

CHECK_NAME = 'neo4j'

METRIC_TAGS = ['tag1', 'tag2']

NEO4J_MINIMAL_CONFIG = {'neo4j_url': URL, 'user': 'neo4j', 'password': 'dog', 'port': '7474'}
NEO4J_AUTH = '{}/{}'.format(NEO4J_MINIMAL_CONFIG['user'], NEO4J_MINIMAL_CONFIG['password'])

CONNECTION_FAILURE = {'neo4j_url': URL, 'user': 'unknown', 'pass': 'dog'}

NEO4J_VARS = [
    'array.store.size',
    'node.ids.inuse',
    'total.store.size',
    'node.store.size',
    'property.ids.inuse',
    'relationshiptype.ids.inuse',
    'property.store.size',
    'store.creationdate',
    'relationship.store.size',
    'kernel.starttime',
    'string.store.size',
    'relationship.ids.inuse',
    'store.log.version',
    'logicallog.size',
]
