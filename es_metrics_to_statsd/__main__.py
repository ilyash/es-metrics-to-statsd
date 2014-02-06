#!/usr/bin/env python
# vim: ts=4 sw=4 et

from __future__ import print_function

import json
import os
import sys
import time

import requests
import statsd

CFG_ENV_VAR = 'ES_METRICS_TO_STATSD_CONFIG'

if CFG_ENV_VAR not in os.environ:
    print(
        "You must supply envronment variable {0} "
        "that points to your config file in JSON "
        "format".format(CFG_ENV_VAR))
    sys.exit(1)

# Config

with open(os.environ['ES_METRICS_TO_STATSD_CONFIG']) as conf_file:
    config = json.load(conf_file)

conf_statsd = {
    'host': 'localhost',
    'port': 8125,
    'prefix': 'ElasticSearch',
}
conf_statsd.update(config.get('statsd', {}))

conf_es = {
    'url': 'http://127.0.0.1:9200',
    'sleep': 5,
}
conf_es.update(config.get('es', {}))


def _extract(data, path, results):
    if isinstance(data, int) and not isinstance(data, bool):
        print(path, data)
        results.append((path, data))
        return
    if isinstance(data, dict):
        for kk, vv in data.items():
            _extract(vv, path + [kk], results)

def extract(data):
    # print(data)
    results = []
    _extract(data, [], results)
    return results


# Prepare

statsd_client = statsd.StatsClient(**conf_statsd)

# Main loop


while True:

    try:
        es_stats = requests.get(conf_es['url'] + '/_status').text
    except:
        # TODO: logging?
        es_stats = None
    if es_stats:
        # print(es_stats)  # XXX
        stats_to_send = extract(json.loads(es_stats))
        for path, v in stats_to_send:
            statsd_client.gauge('.'.join(path), v)
    time.sleep(conf_es['sleep'])
