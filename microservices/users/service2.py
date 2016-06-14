import json
from argparse import ArgumentParser
from socket import gethostname

from flask import Flask, jsonify, request
from sqlalchemy.exc import DatabaseError

from database import db_session
from models import User

app = Flask(__name__)

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


class ApiError(Exception):
    def __init__(self):
        pass

    def to_dict(self):
        raise NotImplementedError()


class InvalidJson(ApiError):
    def __init__(self, json):
        super(InvalidJson, self).__init__()
        self.message = 'Invalid user json!'
        self.status_code = 400
        self.json = json

    def to_dict(self):
        return {
            'status': 'error',
            'message': self.message,
            'json': self.json,
            'code': self.status_code
        }


class InvalidArgument(ApiError):
    def __init__(self, msg):
        super(InvalidArgument, self).__init__()
        self.message = msg
        self.status_code = 400

    def to_dict(self):
        return {
            'status': 'error',
            'message': self.message,
            'code': self.status_code
        }


def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'ip': user.ip
    }


def user_from_dict(dictionary):
    return User(dictionary['name'], dictionary['email'], dictionary['ip'])


@app.route('/')
def users_info():
    return jsonify({'service': 'users'})


@app.route('/users', methods=['POST'])
def users_add():
    try:
        user_json = json.loads(request.data)
    except:
        raise InvalidJson('Parsing error!')
    if 'name' not in user_json or 'email' not in user_json or 'ip' not in user_json:
        raise InvalidJson(user_json)
    user = user_from_dict(user_json)
    db_session.add(user)
    db_session.commit()
    return jsonify({'status': 'ok', 'id': user.id})


@app.route('/users/<id>', methods=['GET'])
def users_get(id):
    try:
        id = int(id)
    except:
        raise InvalidArgument('Id must be an integer value!')
    user = User.query.filter(User.id == id).first()
    if not user:
        raise InvalidArgument('No such user in database!')
    return jsonify({'status': 'ok', 'user': user_to_dict(user)})


@app.route('/users', methods=['GET'])
def users_all():
    users = User.query.all()
    return jsonify({'status': 'ok', 'users': [user_to_dict(user) for user in users]})


@app.route('/users/name/<name>')
def users_by_name(name):
    users = User.query.filter(User.name.like('%%%s%%' % name))
    return jsonify({'status': 'ok', 'users': [user_to_dict(user) for user in users]})


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(DatabaseError)
def handle_database_error(error):
    response = jsonify({
        'status': 'error',
        'code': 400,
        'error': error.message
    })
    response.status_code = 400
    return response


if __name__ == '__main__':
    parser = ArgumentParser(description='Runs the users service.')
    parser.add_argument('--host', help='Specifies the host for the application.',
                        default='127.0.0.1')
    parser.add_argument('--port', type=int, help='Specifies the port for the application.',
                        default=5000)
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port)
