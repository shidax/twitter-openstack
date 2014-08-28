#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python;Encoding: utf8n -*-

import os
import sys
import logging
import logging.config
import ConfigParser


log = logging.getLogger(__name__)

def load_config(path):
    conf = ConfigParser.SafeConfigParser()
    conf.read(path)
    return conf

