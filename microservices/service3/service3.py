from __future__ import generators

from argparse import ArgumentParser

import requests
from flask import Flask, jsonify

app = Flask(__name__)

users_endpoint = ''
ip_endpoint = ''


@app.route('/<name>')
def aggregate_name(name):
    user_request = requests.get('%s/users/name/%s' % (users_endpoint, name))
    users = user_request.json()['users']
    ip_requests = [requests.get('%s/%s' % (ip_endpoint, user['ip'])) for user in users]
    ip_results = [r.json() for r in ip_requests]
    return jsonify({
        'status': 'ok',
        'users': [{'user': users[i], 'diagnostic': ip_results[i]} for i in range(len(users))]
    })


@app.route('/')
def aggregate_info():
    return jsonify({'service': 'aggregate'})


@app.errorhandler(requests.RequestException)
def http_error(error):
    response = jsonify({
        'status': 'error',
        'code': 500,
        'error': error.message
    })
    response.status_code = 500
    return response


if __name__ == '__main__':
    parser = ArgumentParser(description='Runs the IP service.')
    parser.add_argument('--host', help='Specifies the host for the application.',
                        default='127.0.0.1')
    parser.add_argument('--port', type=int, help='Specifies the port for the application.',
                        default=5000)
    parser.add_argument('-u', '--users', help='Specifies the address to the users service.',
                        required=True)
    parser.add_argument('-i', '--ip', help='Specifies the address to the ip service.',
                        required=True)
    arguments = parser.parse_args()
    users_endpoint = arguments.users
    ip_endpoint = arguments.ip
    app.run(host=arguments.host, port=arguments.port)
