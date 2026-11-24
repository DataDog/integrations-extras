import os

HERE = os.path.dirname(os.path.abspath(__file__))

COMMON_METRICS = [
    'hugging_face_tei.batch.next.size.bucket',
    'hugging_face_tei.batch.next.size.count',
    'hugging_face_tei.batch.next.size.sum',
    'hugging_face_tei.batch.next.tokens.bucket',
    'hugging_face_tei.batch.next.tokens.count',
    'hugging_face_tei.batch.next.tokens.sum',
    'hugging_face_tei.queue.size',
    'hugging_face_tei.request.count',
    'hugging_face_tei.request.duration.bucket',
    'hugging_face_tei.request.duration.count',
    'hugging_face_tei.request.duration.sum',
    'hugging_face_tei.request.failure.count',
    'hugging_face_tei.request.inference.duration.bucket',
    'hugging_face_tei.request.inference.duration.count',
    'hugging_face_tei.request.inference.duration.sum',
    'hugging_face_tei.request.input_length.bucket',
    'hugging_face_tei.request.input_length.count',
    'hugging_face_tei.request.input_length.sum',
    'hugging_face_tei.request.queue.duration.bucket',
    'hugging_face_tei.request.queue.duration.count',
    'hugging_face_tei.request.queue.duration.sum',
    'hugging_face_tei.request.success.count',
    'hugging_face_tei.request.tokenization.duration.bucket',
    'hugging_face_tei.request.tokenization.duration.count',
    'hugging_face_tei.request.tokenization.duration.sum',
]

EMBEDDING_METRICS = COMMON_METRICS + [
    'hugging_face_tei.embed.count',
    'hugging_face_tei.embed.duration.bucket',
    'hugging_face_tei.embed.duration.count',
    'hugging_face_tei.embed.duration.sum',
    'hugging_face_tei.embed.inference.duration.bucket',
    'hugging_face_tei.embed.inference.duration.count',
    'hugging_face_tei.embed.inference.duration.sum',
    'hugging_face_tei.embed.queue.duration.bucket',
    'hugging_face_tei.embed.queue.duration.count',
    'hugging_face_tei.embed.queue.duration.sum',
    'hugging_face_tei.embed.success.count',
    'hugging_face_tei.embed.tokenization.duration.bucket',
    'hugging_face_tei.embed.tokenization.duration.count',
    'hugging_face_tei.embed.tokenization.duration.sum',
]

RERANK_METRICS = COMMON_METRICS + [
    'hugging_face_tei.predict.count',
    'hugging_face_tei.predict.duration.bucket',
    'hugging_face_tei.predict.duration.count',
    'hugging_face_tei.predict.duration.sum',
    'hugging_face_tei.predict.inference.duration.bucket',
    'hugging_face_tei.predict.inference.duration.count',
    'hugging_face_tei.predict.inference.duration.sum',
    'hugging_face_tei.predict.queue.duration.bucket',
    'hugging_face_tei.predict.queue.duration.count',
    'hugging_face_tei.predict.queue.duration.sum',
    'hugging_face_tei.predict.success.count',
    'hugging_face_tei.predict.tokenization.duration.bucket',
    'hugging_face_tei.predict.tokenization.duration.count',
    'hugging_face_tei.predict.tokenization.duration.sum',
]

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:8080/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
