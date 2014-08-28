#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python;Encoding: utf8n -*-
import logging
import json
import datetime

import eventlet

from tweetstack import handler
from tweetstack import logger

log = logging.getLogger(__name__)

class DataStore(object):

    def __init__(self, conf):
        self.conf = conf

    def store(self, data):
        pass

    def countup(self):
        pass

    def start_time(self):
        pass

    def get(self):
        pass

    def count(self):
        pass


class MemoryDataStore(DataStore):

    def __init__(self, conf):
        DataStore.__init__(self, conf)
        self.data = []
        self.count = 0
        self.start = datetime.datetime.today()

    def store(self, data):
        self.data.append(data)

    def countup(self):
        self.count = self.count + 1

    def start_time(self):
        return self.start

    def get(self):
        return self.data

    def get_count(self):
        return self.count
