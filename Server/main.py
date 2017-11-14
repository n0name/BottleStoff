from flask import Flask, request, make_response, jsonify
from sqlobject import *
import uuid

sqlhub.processConnection = connectionForURI('sqlite:/users.db')


class User(SQLObject):
    name = StringCol()
    password = StringCol()


class UserInfo(SQLObject):
    pass


User.createTable(ifNotExists=True)

server = Flask(__name__)


def check_fields(request_json, *fields):
    for field in fields:
        if field not in request_json:
            return False
    return True


def required_fields(*fields):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if not request.json:
                return make_response(jsonify({"error": "Non Json Input"}), 400)

            if not check_fields(request.json, *fields):
                return make_response(jsonify({"error": "invalid input"}), 400)

            return function(*args, **kwargs)

        return wrapper

    return real_decorator


_ActiveUsers = {}


@server.route('/login', methods=['POST'])
@required_fields('user_name', 'password')
def login():
    user_name = request.json['user_name']
    password = request.json['password']

    found = User.select(User.q.name == user_name)

    if found.count() > 0:
        for user in found:
            if user.password == password:
                the_user = user
                break
        else:
            return make_response(jsonify({'Error': "Incorrect Password"}), 400)
    else:
        # Create user
        the_user = User(name=user_name, password=password)

    if the_user:
        token = str(uuid.uuid4())
        _ActiveUsers.update({token: UserInfo()})
        return make_response(jsonify({
            "token": token
        }), 200)

    pass


if __name__ == '__main__':
    server.run(port=8080, debug=True)
