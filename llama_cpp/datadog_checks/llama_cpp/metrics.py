METRIC_MAP = {
    ## Prompt processing
    'llamacpp:prompt_tokens': 'prompt_tokens',
    'llamacpp:prompt_tokens_cached': 'prompt_tokens_cached',
    'llamacpp:prompt_seconds': 'prompt_seconds',
    'llamacpp:prompt_tokens_seconds': 'prompt_tokens_per_second',
    ## Generation
    'llamacpp:tokens_predicted': 'tokens_predicted',
    'llamacpp:tokens_predicted_seconds': 'tokens_predicted_seconds',
    'llamacpp:predicted_tokens_seconds': 'predicted_tokens_per_second',
    ## Decoding
    'llamacpp:n_decode': 'decode_calls',
    'llamacpp:n_busy_slots_per_decode': 'busy_slots_per_decode',
    # Exposed with the counter type, but it holds the largest observed sequence length.
    'llamacpp:n_tokens_max': {'name': 'tokens_max', 'type': 'gauge'},
    ## Requests
    'llamacpp:requests_processing': 'requests.processing',
    'llamacpp:requests_deferred': 'requests.deferred',
    ## Speculative decoding
    'llamacpp:spec_decode_num_draft_tokens': 'spec_decode.draft_tokens',
    'llamacpp:spec_decode_num_accepted_tokens': 'spec_decode.accepted_tokens',
    'llamacpp:spec_decode_num_drafts': 'spec_decode.drafts',
}
