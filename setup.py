#!/usr/bin/env python

from setuptools import setup

setup(name = 'es_metrics_to_statsd',
      version = '0.1',
      description = 'ElasticSearch metrics to statsd',
      author = 'Ilya Sher',
      author_email = 'ilya.sher@coding-knight.com',
      packages = ['es_metrics_to_statsd'],
      install_requires = ['requests', 'statsd'],
      zip_safe = True,
      classifiers = [
          "Development Status :: 3 - Alpha",
      ])
