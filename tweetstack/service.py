#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python;Encoding: utf8n -*-
import logging
import json
import time

import eventlet

from tweetstack import handler
from tweetstack import logger
from tweetstack import pipeline
from tweetstack import datastore
from tweetstack import commands

log = logging.getLogger(__name__)

class Service(object):

    def __init__(self, conf):
        self.conf = conf
        self.follows = conf.get('twitter', 'follows')

    def run(self):
        command = commands.Command(self.conf)
        store = datastore.MemoryDataStore(self.conf)
        pipe = pipeline.build(self.conf, store, command)
        self.handle_twitter(pipe)

    def handle_twitter(self, pipe):
        conn = handler.TwitterConnection(self.conf)
        stream = conn.connect(pipe)
        stream.statuses.filter(follow=self.follows)

