import json


def read_file(file_path, is_json=False):
    with open(file_path, "r") as f:
        return json.load(f) if is_json else f.read()


OM_METRICS = [
    "qdrant.app.status.recovery.mode",
    "qdrant.collections.total",
    "qdrant.collections.vector.total",
    "qdrant.rest.responses.avg.duration.seconds",
    "qdrant.rest.responses.min.duration.seconds",
    "qdrant.rest.responses.max.duration.seconds",
    "qdrant.grpc.responses.avg.duration.seconds",
    "qdrant.grpc.responses.min.duration.seconds",
    "qdrant.grpc.responses.max.duration.seconds",
    "qdrant.cluster.enabled",
    "qdrant.cluster.peers.total",
    "qdrant.cluster.term.count",
    "qdrant.cluster.commit.count",
    "qdrant.cluster.pending.operations.total",
    "qdrant.cluster.voter",
    "qdrant.grpc.responses.count",
    "qdrant.grpc.responses.fail.count",
    "qdrant.rest.responses.count",
    "qdrant.rest.responses.fail.count",
]
