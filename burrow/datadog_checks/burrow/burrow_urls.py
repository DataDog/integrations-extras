from __future__ import absolute_import
from six.moves.urllib.parse import urljoin


def burrow_admin(base):
    """
    /burrow/admin
    """
    return urljoin(base, "burrow/admin")
def clusters(base):
    """
    /v3/kafka
    """
    return urljoin(base, "v3/kafka")
def cluster(base, cluster_name):
    """
    /v3/kafka/{cluster_name}
    """
    return "%s/%s" % (clusters(base), cluster_name)
def consumers(base, cluster_name):
    """
    /v3/kafka/{cluster_name}/consumer
    """
    return "%s/%s" % (cluster(base, cluster_name), "consumer")
def consumer(base, cluster_name, consumer_group_name):
    """
    /v3/kafka/{cluster_name}/consumer/{consumer_group_name}
    """
    return "%s/%s" % (consumers(base, cluster_name), consumer_group_name)
def consumer_status(base, cluster_name, consumer_group_name):
    """
    /v3/kafka/{cluster_name}/consumer/{consumer_group_name}/status
    """
    return "%s/%s" % (consumer(base, cluster_name, consumer_group_name), "status")
def consumer_lag(base, cluster_name, consumer_group_name):
    """
    /v3/kafka/{cluster_name}/consumer/{consumer_group_name}/lag
    """
    return "%s/%s" % (consumer(base, cluster_name, consumer_group_name), "lag")
def topics(base, cluster_name):
    """
    /v3/kafka/{cluster_name}/topic
    """
    return "%s/%s" % (cluster(base, cluster_name), "topic")
def topic(base, cluster_name, topic_name):
    """
    /v3/kafka/{cluster_name}/topic/{topic_name}
    """
    return "%s/%s" % (topics(base, cluster_name), topic_name)
