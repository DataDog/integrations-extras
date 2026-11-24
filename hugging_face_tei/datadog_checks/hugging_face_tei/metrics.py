METRIC_MAP = {
    ## Requests
    'te_request_count': 'request',
    'te_request_success': 'request.success',
    'te_request_failure': 'request.failure',
    'te_request_duration': 'request.duration',
    'te_request_input_length': 'request.input_length',
    'te_request_tokenization_duration': 'request.tokenization.duration',
    'te_request_queue_duration': 'request.queue.duration',
    'te_request_inference_duration': 'request.inference.duration',
    ## Queue and batching
    'te_queue_size': 'queue.size',
    'te_batch_next_size': 'batch.next.size',
    'te_batch_next_tokens': 'batch.next.tokens',
    ## Embedding models
    'te_embed_count': 'embed',
    'te_embed_success': 'embed.success',
    'te_embed_duration': 'embed.duration',
    'te_embed_tokenization_duration': 'embed.tokenization.duration',
    'te_embed_queue_duration': 'embed.queue.duration',
    'te_embed_inference_duration': 'embed.inference.duration',
    ## Sequence classification and re-ranker models
    'te_predict_count': 'predict',
    'te_predict_success': 'predict.success',
    'te_predict_duration': 'predict.duration',
    'te_predict_tokenization_duration': 'predict.tokenization.duration',
    'te_predict_queue_duration': 'predict.queue.duration',
    'te_predict_inference_duration': 'predict.inference.duration',
}

RENAME_LABELS_MAP = {
    'err': 'error_type',
}
