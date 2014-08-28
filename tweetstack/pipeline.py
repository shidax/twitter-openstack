#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python;Encoding: utf8n -*-
import logging
import json
import time

import eventlet

from tweetstack import handler
from tweetstack import logger

log = logging.getLogger(__name__)

class Pipeline(object):

    def __init__(self, conf):
        self.conf = conf

    def pipe(self, handler):
        self.handler = handler
        return handler

    def handle(self, data):
        return True

    def next(self, data):
        if self.handle(data) and self.handler:
            self.handler.next(data)


class Counter(Pipeline):

    def __init__(self, conf, datastore):
        Pipeline.__init__(self, conf)
        self.datastore = datastore

    def handle(self, data):
        log.debug("Start count handler")
        self.datastore.countup()
        log.info("Total count of tweet is %d" % self.datastore.get_count())
        return True


class Matcher(Pipeline):

    def __init__(self, conf, datastore):
        Pipeline.__init__(self, conf)
        self.datastore = datastore
        self.keywords = conf.get('default', 'keywords').split(',')

    def handle(self, data):
        log.debug("Start matcher handler")
        text = data['text'].encode('utf8')
        for keyword in self.keywords:
            if keyword in text:
                log.debug("Match keyword %s: in %s" % (keyword, text))
                self.store(keyword, data)
                return True
        return False

    def store(self, keyword, data):
        self.datastore.store(data)


class Executor(Pipeline):

    def __init__(self, conf, command):
        Pipeline.__init__(self, conf)
        self.tenant = conf.get('default', 'tenant_name')
        self.command = command

    def handle(self, data):
        log.debug("Start execute handler")
        user = data['user']['screen_name'].encode('utf8')
        log.info("Boot a new server for %s" % user)
        vm = self.command.assign(user, user, "A new instance for %s" % user)
        return True


class Feedback(Pipeline):

    template = "@%s\n %s さんのオプスタへの情熱に答えて、ウチのクラウドにVM一台起動しておきました"

    def __init__(self, conf):
        Pipeline.__init__(self, conf)

    def handle(self, data):
        log.debug("Start feedback handler")
        user = data['user']['screen_name']
        name = data['user']['name'].encode('utf8')
        status = self.template % (user, name)
        twitter = handler.TwitterConnection(self.conf).twitter()
        twitter.update_status(status=status, in_reply_to_status_id=data['id'])


def build(conf, datastore, command):
    counter = Counter(conf, datastore)
    counter.pipe(Matcher(conf, datastore)).pipe(Executor(conf, command)).pipe(Feedback(conf))
    return counter
