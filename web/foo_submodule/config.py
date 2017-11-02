#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get the configuration.

Default values are defined in config.json. They can be overwritten by
environment variables.
"""

import json
import os

script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, 'config.json')
with open(config_path) as json_data_file:
    cfg = json.load(json_data_file)

if os.environ.get('MYSQL_ROOT_PASSWORD') is not None:
    cfg['db']['username'] = 'root'
    cfg['db']['password'] = os.environ.get('MYSQL_ROOT_PASSWORD')

if os.environ.get('MYSQL_DATABASE') is not None:
    cfg['db']['dbname'] = os.environ.get('MYSQL_DATABASE')

if os.environ.get('MYSQL_HOST') is not None:
    cfg['db']['host'] = os.environ.get('MYSQL_HOST')

if os.environ.get('MYSQL_PORT') is not None:
    cfg['db']['port'] = os.environ.get('MYSQL_PORT')
