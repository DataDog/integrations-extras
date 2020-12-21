<?php
// simple implementation
header("Content-type: text/plain");

$cache = apcu_cache_info(true);
$mem = apcu_sma_info(true);

$prefix = 'php_apcu.';

$results = [
//    'version'            => phpversion('apcu'),
    'cache.mem_size'     => $cache['mem_size'],
    'cache.num_slots'    => $cache['num_slots'],
    'cache.ttl'          => $cache['ttl'],
    'cache.num_hits'     => $cache['num_hits'],
    'cache.num_misses'   => $cache['num_misses'],
    'cache.num_inserts'  => $cache['num_inserts'],
    'cache.num_entries'  => $cache['num_entries'],
    'cache.num_expunges' => isset($cache['expunges']) ? $cache['expunges'] : $cache['num_expunges'],
    'cache.uptime'       => time() - $cache['start_time'],
    'sma.avail_mem'      => $mem['avail_mem'],
    'sma.seg_size'       => $mem['seg_size'],
    'sma.num_seg'        => $mem['num_seg'],
];

foreach ($results as $key => $val) {
    printf("%s %s\n", $prefix . $key, $val);
}
