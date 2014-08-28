#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python;Encoding: utf8n -*-
import logging
import json

from keystoneclient.v3 import client as keystone_client
from keystoneclient import session
from keystoneclient.v3.client import v3_auth
from novaclient import v3 as nova_client

from tweetstack import logger

log = logging.getLogger(__name__)

class Command(object):

    def __init__(self, conf):
        self.conf = conf
        self.domain = conf.get('openstack', 'domain')
        self.role = conf.get('openstack', 'role')
        self.image = conf.get('openstack', 'image')
        self.flavor = conf.get('openstack', 'flavor')
        self.keystone_client = keystone_client.Client(
                               user_domain_name=conf.get('openstack', 'domain'),
                               username=conf.get('openstack', 'user'),
                               password=conf.get('openstack', 'password'),
                               project_domain_name=conf.get('openstack', 'domain'),
                               project_name=conf.get('openstack', 'project'),
                               auth_url=conf.get('openstack', 'auth_url'))

    def create_tenant(self, name):
        projects = self.keystone_client.projects.list(name=name)
        if not projects:
            return self.keystone_client.projects.create(name, self.domain)
        return projects.pop()

    def create_user(self, tenant, name):
        users = self.keystone_client.users.list(name=name)
        if not users:
            user = self.keystone_client.users.create(name=name,
                                                     domain=self.domain,
                                                     password=name,
                                                     default_project=tenant.id)
            role = self.keystone_client.roles.list(name=self.role).pop()
            self.keystone_client.roles.grant(role.id, user=user.id, project=tenant.id)
            return user
        return users.pop()

    def boot(self, tenant, user, name):
        token = keystone_client.Client(
                               user_domain_name=self.domain,
                               username=user.name,
                               password=user.name,
                               project_domain_name=self.domain,
                               project_name=tenant.name,
                               auth_url=self.conf.get('openstack', 'auth_url'))
        t = v3_auth.Token(self.conf.get('openstack', 'auth_url'), token.auth_token)
        sess = session.Session(auth=t)
        nova = nova_client.Client(session=sess)
        return nova.servers.create(name, self.image, self.flavor)

    def assign(self, tenant_name, user_name, server_name):
        tenant = self.create_tenant(tenant_name)
        user = self.create_user(tenant, user_name)
        return self.boot(tenant, user, server_name) 


def test(conf, tenant_name, user_name, server_name):
    command = Command(conf)
    tenant = command.create_tenant(tenant_name)
    user = command.create_user(tenant, user_name)
    return command.boot(tenant, user, server_name)
