#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python;Encoding: utf8n -*-
import logging
import json
import time

from tweetstack import logger
from twython import TwythonStreamer
from twython import Twython

log = logging.getLogger(__name__)

class Streamer(TwythonStreamer):

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline

    def on_success(self, data):
        time.sleep(0)
        if 'text' in data:
            text = data['text']
            log.debug(text.encode('utf8'))
            self.pipeline.next(data)

    def on_error(self, status_code, data):
        print status_code, data

class TwitterConnection(object):

    def __init__(self, conf):
        self.consumer_key = conf.get('twitter', 'consumer_key')
        self.consumer_secret = conf.get('twitter', 'consumer_secret')
        self.access_token = conf.get('twitter', 'access_token')
        self.access_token_secret = conf.get('twitter', 'access_token_secret')

    def connect(self, pipe):
        stream = Streamer(self.consumer_key,
                          self.consumer_secret,
                          self.access_token,
                          self.access_token_secret)
        stream.set_pipeline(pipe)
        return stream

    def twitter(self):
        twitter = Twython(self.consumer_key,
                          self.consumer_secret,
                          self.access_token,
                          self.access_token_secret)
        return twitter
