#!/usr/bin/env python
import os
import sys
from time import sleep
from threading import Thread

import django
from django.db import transaction

import docker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netstatus.settings")
django.setup()

from dashboard.models import Flow, Protocols, Risks

client = docker.Client.from_env()

containers = {}
services = {
    '10.10.10.1': 'gateway',
    '10.10.10.254': 'lb',
    '10.42.4.1': 'dashboard',
}

def handle_start(container_id):
    container = client.inspect_container(container_id)
    if container['Config']['Labels'].get('com.docker.compose.project') != 'microservices':
        return
    service = container['Config']['Labels']['com.docker.compose.service']
    suutip_network = container['NetworkSettings']['Networks'].get('suutip')
    if not suutip_network:
        return
    ip_addr = suutip_network['IPAddress']
    containers[container_id] = ip_addr
    services[ip_addr] = service

def handle_stop(container_id):
    ip_addr = containers[container_id]
    del containers[container_id]
    del services[ip_addr]

for container in client.containers():
    container_id = container['Id']
    handle_start(container_id)
print(containers)
print(services)
print('---')

def handle_docker_events():
    for event in client.events(decode=True):
        if event['Type'] != 'container':
            continue
        if event['Action'] not in ('start', 'stop'):
            continue
        container_id = event['Actor']['ID']
        print(event['Type'], event['Action'], container_id)
        if event['Action'] == 'start':
            handle_start(container_id)
        elif event['Action'] == 'stop':
            handle_stop(container_id)
        print(containers)
        print(services)
        print('---')

t = Thread(target=handle_docker_events)
t.daemon = True
t.start()

from random import randint

def calculate_risk(flow):
    src_ip = flow.source_ip
    dst_ip = flow.target_ip
    proto = flow.protocol
    src_port = flow.source_port
    dst_port = flow.target_port
    src_srv = services.get(src_ip, 'external')
    dst_srv = services.get(dst_ip, 'external')
    flow.source = src_srv
    flow.target = dst_srv
    flow.risk = Risks.neutral.value
    if src_srv == 'gateway':
        if proto == Protocols.ARP.value and src_port == 2: flow.risk = Risks.low.value
        #                                               ^- ARP Reply
        else: flow.risk = Risks.high.value
    elif src_srv == 'lb':
        if dst_srv in ('ipdiag', 'users', 'aggregate'):
            if proto == Protocols.TCP.value and dst_port == 5000: flow.risk = Risks.low.value
            elif proto == Protocols.ARP.value: flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'gui':
            if proto == Protocols.TCP.value and dst_port == 3001: flow.risk = Risks.low.value
            elif proto == Protocols.ARP.value: flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'dashboard':
            if proto == Protocols.TCP.value and dst_port in (8008, 8009): flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'external':
            if proto == Protocols.TCP.value and src_port in (80, 443): flow.risk = Risks.moderate.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'gateway':
            if proto == Protocols.ARP.value and src_port == 1: flow.risk = Risks.neutral.value
            #                                               ^- ARP Request
            else: flow.risk = Risks.high.value
        else: flow.risk = Risks.high.value
    elif src_srv == 'ipdiag':
        if dst_srv in ('lb', 'aggregate'):
            if proto == Protocols.TCP.value and src_port == 5000: flow.risk = Risks.low.value
            elif proto == Protocols.ARP.value: flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'external':
            if proto == Protocols.ICMP.value and src_port == 8: flow.risk = Risks.moderate.value
            #                                                ^- Echo Request
            else: flow.risk = Risks.high.value
        elif dst_srv == 'gateway':
            if proto == Protocols.ARP.value and src_port == 1: flow.risk = Risks.neutral.value
            #                                               ^- ARP Request
            else: flow.risk = Risks.high.value
        else: flow.risk = Risks.high.value
    elif src_srv == 'users':
        if dst_srv in ('lb', 'aggregate'):
            if proto == Protocols.TCP.value and src_port == 5000: flow.risk = Risks.low.value
            elif proto == Protocols.ARP.value: flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'db':
            if proto == Protocols.TCP.value and dst_port == 5432: flow.risk = Risks.low.value
            elif proto == Protocols.ARP.value: flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'gateway':
            if proto == Protocols.ARP.value and src_port == 1: flow.risk = Risks.neutral.value
            #                                               ^- ARP Request
            else: flow.risk = Risks.high.value
        else: flow.risk = Risks.high.value
    elif src_srv == 'aggregate':
        if dst_srv == 'lb':
            if proto == Protocols.TCP.value and src_port == 5000: flow.risk = Risks.low.value
            elif proto == Protocols.ARP.value: flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv in ('ipdiag', 'users'):
            if proto == Protocols.TCP.value and dst_port == 5000: flow.risk = Risks.low.value
            elif proto == Protocols.ARP.value: flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'gateway':
            if proto == Protocols.ARP.value and src_port == 1: flow.risk = Risks.neutral.value
            #                                               ^- ARP Request
            else: flow.risk = Risks.high.value
        else: flow.risk = Risks.high.value
    elif src_srv == 'gui':
        if dst_srv == 'lb':
            if proto == Protocols.TCP.value and src_port == 3001: flow.risk = Risks.low.value
            elif proto == Protocols.ARP.value: flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'gateway':
            if proto == Protocols.ARP.value and src_port == 1: flow.risk = Risks.neutral.value
            #                                               ^- ARP Request
            else: flow.risk = Risks.high.value
        else: flow.risk = Risks.high.value
    elif src_srv == 'db':
        if dst_srv == 'users':
            if proto == Protocols.TCP.value and src_port == 5432: flow.risk = Risks.low.value
            elif proto == Protocols.ARP.value: flow.risk = Risks.low.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'gateway':
            if proto == Protocols.ARP.value and src_port == 1: flow.risk = Risks.neutral.value
            #                                               ^- ARP Request
            else: flow.risk = Risks.high.value
        else: flow.risk = Risks.high.value
    elif src_srv == 'external':
        if dst_srv == 'gateway': flow.risk = Risks.high.value
        elif dst_srv == 'lb':
            if proto == Protocols.TCP.value and dst_port in (80, 443): flow.risk = Risks.moderate.value
            else: flow.risk = Risks.high.value
        elif dst_srv == 'ipdiag':
            if proto == Protocols.ICMP.value and src_port == 0: flow.risk = Risks.moderate.value
            #                                                ^- Echo Reply
            else: flow.risk = Risks.high.value
        else: flow.risk = Risks.high.value
    elif src_srv == 'dashboard':
        if dst_srv == 'lb':
            if proto == Protocols.TCP.value and src_port in (8008, 8009): flow.risk = Risks.moderate.value
            else: flow.risk = Risks.high.value
        else: flow.risk = Risks.high.value        
    else: flow.risk = Risks.high.value
    flow.save()

try:
    while True:
        for flow in Flow.objects.filter(risk=Risks.unrated.value):
            print(flow.id, flow.protocol, flow.source_ip, flow.target_ip)
            calculate_risk(flow)
        sleep(5)
except KeyboardInterrupt:
    exit()
