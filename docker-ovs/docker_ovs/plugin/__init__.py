from docker_ovs.flask_utils import make_json_app
from docker_ovs.plugin.rand_utils import get_rand_mac
from docker_ovs.plugin.endpoint_utils import create_endpoint, delete_endpoint

import json
import logging
import os
import requests
import shelve
import sys

from flask import jsonify, request


DOCKER_OVS_BRIDGE = os.environ.get('DOCKER_OVS_BRIDGE', 'obr0')
DOCKER_OVS_CENTRAL = os.environ.get('DOCKET_OVS_CENTRAL', 'http://10.42.4.1:5000')

db = shelve.open('docker_ovs.db')
if 'endpoints' not in db:
    db['endpoints'] = {}

app = make_json_app(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)
app.logger.info('Docker Open vSwitch plugin started')


@app.route('/Plugin.Activate', methods=['POST'])
def net_drv_plugin_activate():
    json_response = {'Implements': ['NetworkDriver']}
    return jsonify(json_response)


@app.route('/NetworkDriver.GetCapabilities', methods=['POST'])
def net_drv_get_capabilities():
    json_response = {'Scope': 'global'}
    return jsonify(json_response)


@app.route('/NetworkDriver.CreateNetwork', methods=['POST'])
def net_drv_create_network():
    json_request = json.loads(request.data)
    json_response = requests.post(DOCKER_OVS_CENTRAL + '/NetworkDriver.CreateNetwork', json=json_request).json()
    return jsonify(json_response)


@app.route('/NetworkDriver.DeleteNetwork', methods=['POST'])
def net_drv_delete_network():
    json_request = json.loads(request.data)
    json_response = requests.post(DOCKER_OVS_CENTRAL + '/NetworkDriver.DeleteNetwork', json=json_request).json()
    return jsonify(json_response)


@app.route('/NetworkDriver.CreateEndpoint', methods=['POST'])
def net_drv_create_endpoint():
    json_response = {
        'Interface': {
            'MacAddress': get_rand_mac(),
        }
    }
    return jsonify(json_response)


@app.route('/NetworkDriver.EndpointOperInfo', methods=['POST'])
def net_drv_endpoint_oper_info():
    json_response = {
        'Value': {},
    }
    return jsonify(json_response)


@app.route('/NetworkDriver.DeleteEndpoint', methods=['POST'])
def net_drv_delete_endpoint():
    json_response = {}
    return jsonify(json_response)


@app.route('/NetworkDriver.Join', methods=['POST'])
def net_drv_join():
    json_request = json.loads(request.data)
    json_response = requests.post(DOCKER_OVS_CENTRAL + '/NetworkDriver.Join', json=json_request).json()
    tag = json_response['Tag']
    host_if, container_if = create_endpoint(DOCKER_OVS_BRIDGE, tag)
    hosts_ifs = db['endpoints']
    hosts_ifs[json_request['EndpointID']] = host_if
    db['endpoints'] = hosts_ifs
    json_response = {
        'InterfaceName': {
            'SrcName': container_if,
            'DstPrefix': 'eth',
        },
        'Gateway': json_response['Gateway'],
        'GatewayIPv6': '',
        'StaticRoutes': [],
    }
    return jsonify(json_response)


@app.route('/NetworkDriver.Leave', methods=['POST'])
def net_drv_leave():
    json_request = json.loads(request.data)
    delete_endpoint(DOCKER_OVS_BRIDGE, db['endpoints'][json_request['EndpointID']])
    hosts_ifs = db['endpoints']
    del hosts_ifs[json_request['EndpointID']]
    db['endpoints'] = hosts_ifs
    json_response = {}
    return jsonify(json_response)


@app.route('/NetworkDriver.DiscoverNew', methods=['POST'])
def net_drv_discover_new():
    json_response = {}
    return jsonify(json_response)


@app.route('/NetworkDriver.DiscoverDelete', methods=['POST'])
def net_drv_discover_delete():
    json_response = {}
    return jsonify(json_response)
