from docker_ovs.flask_utils import make_json_app

import json
import logging
import os
from random import choice
import shelve
import sys

from flask import jsonify, request


db = shelve.open('docker_ovs.db')
if 'vlans' not in db:
    db['vlans'] = set(xrange(1, 4095))
if 'networks' not in db:
    db['networks'] = {}

app = make_json_app(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)
app.logger.info('Docker Open vSwitch central started')


@app.route('/NetworkDriver.CreateNetwork', methods=['POST'])
def create_network():
    json_request = json.loads(request.data)
    network_id = json_request['NetworkID']
    gateway_ip = json_request['IPv4Data'][0]['Gateway']
    if network_id not in db['networks']:
        networks = db['networks']
        vlans = db['vlans']
        networks[network_id] = {'Tag': vlans.pop(), 'Gateway': gateway_ip}
        db['networks'] = networks
        db['vlans'] = vlans
    json_response = {}
    return jsonify(json_response)


@app.route('/NetworkDriver.DeleteNetwork', methods=['POST'])
def delete_network():
    json_request = json.loads(request.data)
    network_id = json_request['NetworkID']
    if network_id in db['networks']:
        networks = db['networks']
        vlans = db['vlans']
        vlans.add(networks[network_id]['Tag'])
        del networks[network_id]
        db['networks'] = networks
        db['vlans'] = vlans
    json_response = {}
    return jsonify(json_response)


@app.route('/NetworkDriver.Join', methods=['POST'])
def join():
    json_request = json.loads(request.data)
    network_id = json_request['NetworkID']
    json_response = db['networks'][network_id]
    return jsonify(json_response)
