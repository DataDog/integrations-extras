import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.checks import AgentCheck
from datadog_checks.win_docker_daemon import WinDockerDaemonCheck

from . import APIMockClient


def test_empty_check(aggregator, instance):
    check = WinDockerDaemonCheck('win_docker_daemon', {}, {})

    with pytest.raises(ConfigurationError):
        check.check(instance)


def test_process_container_totals(aggregator, instance):

    check = WinDockerDaemonCheck('win_docker_daemon', {}, {})
    instance = {'url': 'http://localhost:2375', 'test_api_client': APIMockClient()}
    check.check(instance)
    # check._process_container_totals(all_containers)
    aggregator.assert_metric('docker.containers.running.total', metric_type=aggregator.GAUGE, value=2, tags=set())
    aggregator.assert_metric('docker.containers.stopped.total', metric_type=aggregator.GAUGE, value=1, tags=set())

    # check._process_container_counts(all_containers)
    aggregator.assert_metric(
        'docker.containers.running',
        metric_type=aggregator.GAUGE,
        value=1,
        tags=['docker_image:my-running-image:latest', 'image_name:my-running-image:latest'],
    )
    aggregator.assert_metric(
        'docker.containers.running',
        metric_type=aggregator.GAUGE,
        value=1,
        tags=[
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )
    aggregator.assert_metric(
        'docker.containers.stopped',
        metric_type=aggregator.GAUGE,
        value=1,
        tags=['docker_image:my-exited-image:1.1.0-alpha.1535.1535', 'image_name:my-exited-image:1.1.0-alpha.1535.1535'],
    )

    # events, service, exit code, and event tollup
    aggregator.assert_service_check(
        'docker.exit',
        count=1,
        status=AgentCheck.CRITICAL,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    # events and rollup
    aggregator.assert_event(
        'my-running-image:latest 1 exec_die, 1 exec_start: cmd , 1 exec_create: cmd',
        exact_match=False,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.service.name:MyRunningImage',
            'docker_image:my-running-image:latest',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'image_name:my-running-image:latest',
        ],
    )

    # sock based stats for "running:
    aggregator.assert_metric(
        'docker.cpu.usage',
        metric_type=aggregator.GAUGE,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.usage',
        metric_type=aggregator.HISTOGRAM,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.system',
        metric_type=aggregator.GAUGE,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.system',
        metric_type=aggregator.HISTOGRAM,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.user',
        metric_type=aggregator.GAUGE,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.user',
        metric_type=aggregator.HISTOGRAM,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.mem.commit',
        metric_type=aggregator.GAUGE,
        value=1066147840.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.mem.commit',
        metric_type=aggregator.HISTOGRAM,
        value=1066147840.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.mem.rss',
        metric_type=aggregator.HISTOGRAM,
        value=839929856.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.mem.rss',
        metric_type=aggregator.HISTOGRAM,
        value=839929856.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'image_name:my-running-image:latest',
        ],
    )

    # network metrics
    aggregator.assert_metric(
        'docker.net.bytes_rcvd',
        metric_type=aggregator.RATE,
        value=22902589939.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'docker_network:3801E41B-4319-49B5-9C79-617B6B81229C',
            'image_name:my-running-image:latest',
        ],
    )

    aggregator.assert_metric(
        'docker.net.bytes_sent',
        metric_type=aggregator.RATE,
        value=1497821969.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyRunningImage',
            'com.docker.swarm.task.id:kvtu1ib57uofp7ompwldwtdxt',
            'com.docker.swarm.task.name:MyRunningImage.2.kvtu1ib57uofp7ompwldwtdxt',
            'container_name:/my-running-image.kvtu1ib57uofp7ompwldwtdxt',
            'docker_image:my-running-image:latest',
            'docker_network:3801E41B-4319-49B5-9C79-617B6B81229C',
            'image_name:my-running-image:latest',
        ],
    )

    # sock based stats for "other running"
    aggregator.assert_metric(
        'docker.cpu.usage',
        metric_type=aggregator.GAUGE,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.usage',
        metric_type=aggregator.HISTOGRAM,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.system',
        metric_type=aggregator.GAUGE,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.system',
        metric_type=aggregator.HISTOGRAM,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.user',
        metric_type=aggregator.GAUGE,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.cpu.user',
        metric_type=aggregator.HISTOGRAM,
        value=0.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.mem.commit',
        metric_type=aggregator.GAUGE,
        value=1069146112.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.mem.commit',
        metric_type=aggregator.HISTOGRAM,
        value=1069146112.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.mem.rss',
        metric_type=aggregator.HISTOGRAM,
        value=848359424.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.mem.rss',
        metric_type=aggregator.HISTOGRAM,
        value=848359424.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    # network metrics
    aggregator.assert_metric(
        'docker.net.bytes_rcvd',
        metric_type=aggregator.RATE,
        value=22917865892.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'docker_network:3801E41B-4319-49B5-9C79-617B6B81229C',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
        ],
    )

    aggregator.assert_metric(
        'docker.net.bytes_sent',
        metric_type=aggregator.RATE,
        value=1498650864.0,
        tags=[
            'com.docker.swarm.node.id:x972iubw3f7s4h9a2s1y79ucc',
            'com.docker.swarm.service.id:jyx7cq6dx5qgvjlh6qng8oqhx',
            'com.docker.swarm.service.name:MyOtherRunningImage',
            'com.docker.swarm.task.id:rsqdvl4j5ihnei2c6drjhqzz0',
            'com.docker.swarm.task.name:MyOtherRunningImage.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'container_name:/my-other-running-image.1.rsqdvl4j5ihnei2c6drjhqzz0',
            'docker_image:my-other-running-image:1.1.0-alpha.136.136',
            'image_name:my-other-running-image:1.1.0-alpha.136.136',
            'docker_network:3801E41B-4319-49B5-9C79-617B6B81229C',
        ],
    )

    # print(aggregator.get('metrics'))
    # print(aggregator.get('service_checks'))
    aggregator.assert_all_metrics_covered()
