<?php
// simple implementation
header("Content-type: text/plain");

$status = opcache_get_status(false);

$prefix = 'php_opcache.';

$results = [];
foreach ($status as $key => $val) {
    if (is_array($val)) {
        foreach ($val as $key2 => $val2) {
            $results[$prefix . $key . '.' . $key2] = _val($val2);
        }
    } else {
        $results[$prefix . $key] = _val($val);
    }
}

foreach ($results as $key => $val) {
    printf("%s %s\n", $key, $val);
}

function _val($val) {
    $tmp = $val;
    if (is_bool($val)) {
        $tmp = intval($val);
    } elseif(is_float($val)) {
        $tmp = round($val, 2);
    }
    return $tmp;
}

