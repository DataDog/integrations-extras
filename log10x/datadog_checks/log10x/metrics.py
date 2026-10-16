# Maps the counters the 10x Engine's Prometheus scrape endpoint serves to the names this
# integration submits. The base class strips the `_total` suffix from counters before
# matching, and submits each counter as `<namespace>.<name>.count`.
#
# Aggregator names come from the engine's shipped aggregate configs:
#   all_events       every event the pipeline read            (receiver)
#   emitted_events   events not routed to drop                 (receiver, reporter)
#   indexed_events   events written to offload storage         (retriever index)
#   streamed_events  events a retrieval query returned         (retriever query stream)
METRIC_MAP = {
    ## Read
    'all_events_summaryVolume': 'events.read',
    'all_events_summaryBytes': 'bytes.read',
    ## Forwarded
    'emitted_events_summaryVolume': 'events.forwarded',
    'emitted_events_summaryBytes': 'bytes.forwarded',
    'emitted_events_optimized_size': 'bytes.encoded',
    ## Offloaded
    'indexed_events_summaryVolume': 'events.offloaded',
    'indexed_events_summaryBytes': 'bytes.offloaded',
    ## Retrieved
    'streamed_events_summaryVolume': 'events.retrieved',
    'streamed_events_summaryBytes': 'bytes.retrieved',
}
