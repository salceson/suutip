import re
from argparse import ArgumentParser
from subprocess import Popen, PIPE

from flask import Flask, jsonify

app = Flask(__name__)
_ip_regex = re.compile('^(\d){1,3}\.(\d){1,3}\.(\d){1,3}\.(\d){1,3}$')


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
    traceroute_cmd = ['traceroute', ip]
    traceroute_process = Popen(traceroute_cmd, stdout=PIPE)
    (traceroute_result, traceroute_error) = traceroute_process.communicate()
    traceroute_exit_code = traceroute_process.wait()
    return jsonify({
        'ping_ok': (ping_exit_code == 0),
        'ping_result': ping_result or '',
        'ping_error': ping_error or '',
        'traceroute_ok': (traceroute_exit_code == 0),
        'traceroute_result': traceroute_result or '',
        'traceroute_error': traceroute_error or ''
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
