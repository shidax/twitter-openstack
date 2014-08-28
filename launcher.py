#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python;Encoding: utf8n -*-

import os
import sys
import logging
import logging.config
import ConfigParser

import eventlet

from tweetstack import config
from tweetstack import handler
from tweetstack import logger
from tweetstack import service

eventlet.monkey_patch()

log = logging.getLogger(__name__)


def main():
    if len(sys.argv) < 2:
        log.info("Please specify the config file. Use default")
        path = 'tweetstack.conf'
    else:
        path = sys.argv[1]

    conf = config.load_config(path)
    serv = service.Service(conf)
    serv.run()

if __name__ == '__main__':
    main()

