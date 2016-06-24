import re
from argparse import ArgumentParser
from socket import gethostname
from subprocess import Popen, PIPE

from flask import Flask, jsonify


app = Flask(__name__)

_ip_regex = re.compile('^(\d){1,3}\.(\d){1,3}\.(\d){1,3}\.(\d){1,3}$')
_hostname = gethostname()
_requests_num = 0


@app.before_request
def increment_requests_num():
    global _requests_num
    _requests_num += 1


@app.route('/favicon.ico')
def favicon():
    return '', 404


@app.route('/healthz')
def healthz():
    return jsonify({
        'status': 'ok',
        'node': _hostname,
        'requests_num': _requests_num,
    })


class InvalidIP(Exception):
    def __init__(self, ip):
        super(InvalidIP, self).__init__()
        self.message = 'Invalid IPv4 address!'
        self.status_code = 400
        self.ip = ip

    def to_dict(self):
        return {
            'message': self.message,
            'ip': self.ip,
            'status_code': self.status_code
        }


@app.route('/<ip>')
def ip_diagnostics(ip):
    if not _ip_regex.match(ip):
        raise InvalidIP(ip)
    ping_cmd = ['ping', '-c', '4', ip]
    ping_process = Popen(ping_cmd, stdout=PIPE)
    (ping_result, ping_error) = ping_process.communicate()
    ping_exit_code = ping_process.wait()
    return jsonify({
        'ping_ok': (ping_exit_code == 0),
        'ping_result': ping_result or '',
        'ping_error': ping_error or ''
    })


@app.route('/')
def ip_info():
    return jsonify({'service': 'ip_diagnostics'})


@app.errorhandler(InvalidIP)
def handle_invalid_ip(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    parser = ArgumentParser(description='Runs the IP service.')
    parser.add_argument('--host', help='Specifies the host for the application.',
                        default='127.0.0.1')
    parser.add_argument('--port', type=int, help='Specifies the port for the application.',
                        default=5000)
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port)
