from flask import Flask, request, make_response, jsonify
import uuid

from Server.route_utils import *
from Server.database_stuff import *

from Common.Map import Map

server = Flask(__name__)

_MAP = Map(300, 300)

_ActiveUsers = {}


@required_fields('user_name', 'password')
@server.route('/login', methods=['POST'])
def login():
    print(request.json)
    user_name = request.json['user_name']
    password = request.json['password']

    found = User.select(User.q.name == user_name)

    if found.count() > 0:
        for user in found:
            if user.password == password:
                the_user = user
                break
        else:
            return error("Incorrect Password")
    else:
        # Create user
        user_info = UserInfo(pos_x=30, pos_y=30)
        the_user = User(name=user_name, password=password, user_data=user_info)

    if the_user:
        token = str(uuid.uuid4())
        _ActiveUsers.update({token: the_user.user_data})
        return ok({"token": token})


_DIRECTIONS = {
    "UP": lambda x, y: (x, y + 1),
    "DOWN": lambda x, y: (x, y - 1),
    "LEFT": lambda x, y: (x - 1, y),
    "RIGHT": lambda x, y: (x + 1, y)
}


@required_fields('token', 'direction')
@server.route('/look', methods=['POST'])
def look():
    token = request.json['token']
    if token not in _ActiveUsers:
        return error("User not logged in")

    direction = request.json['direction']
    if direction not in _DIRECTIONS:
        return error("Incorrect Direction : {}".format(direction))

    user_data = _ActiveUsers[token]
    tile = _MAP.get(*_DIRECTIONS[direction](user_data.pos_x, user_data.pos_y))
    if tile:
        return ok({'description': tile.description()})
    else:
        return error('Invalid tile position')


@required_fields('token', 'direction')
@server.route('/move', methods=['POST'])
def move():
    token = request.json['token']
    if token not in _ActiveUsers:
        return error("User not logged in")

    direction = request.json['direction']
    if direction not in _DIRECTIONS:
        return error("Incorrect Direction : {}".format(direction))

    user_data = _ActiveUsers[token]
    tile = _MAP.get(*_DIRECTIONS[direction](user_data.pos_x, user_data.pos_y))
    if tile:
        if tile.is_movable():
            user_data.pos_x, user_data.pos_y = _DIRECTIONS[direction](user_data.pos_x, user_data.pos_y)
            return ok({'description': tile.description()})
        else:
            return error("You can't pass")
    else:
        return error('Invalid tile position')


if __name__ == '__main__':
    server.run('0.0.0.0', port=8080, debug=True)
