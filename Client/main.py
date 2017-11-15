import requests
import json


class Direction:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


_HEADERS = {'Content-Type': 'application/json'}


class ServerConnection:
    def __init__(self, base_address):
        self.base_address = base_address
        self.token = None

    def _make_command(self, cmd):
        return "{}/{}".format(self.base_address, cmd)

    def _exec_command(self, cmd, data):
        url = self._make_command(cmd)
        response = requests.post(url, data=json.dumps(data), headers=_HEADERS)
        resp_data = response.json()
        if response.status_code != 200:
            print(resp_data['Error'])
            return None
        else:
            return resp_data

    def login(self, user, password):
        data = {
            "user_name": user,
            "password": password
        }
        resp = self._exec_command('login', data)
        if resp:
            self.token = resp['token']
            return True
        else:
            return False

        # url = self._make_command('login')
        # response = requests.post(url, data=json.dumps(data), headers=_HEADERS)
        # resp_data = response.json()
        # if response.status_code != 200:
        #     print(resp_data['Error'])
        #     return False
        # else:
        #     self.token = resp_data['token']
        #     return True

    def look(self, direction):
        data = {'token': self.token, 'direction': direction}
        url = self._make_command('look')
        response = requests.post(url, data=json.dumps(data), headers=_HEADERS)
        resp_data = response.json()
        if response.status_code != 200:
            print(resp_data['Error'])
        else:
            print(resp_data['description'])


_COMMAND_HANDLERS = {}
_CONNECTION = ServerConnection('http://localhost:8080')
_RUNNING = True


def command_handler(cmd_name):
    def command_handler_imp(function):
        _COMMAND_HANDLERS.update({cmd_name: function})

    return command_handler_imp


@command_handler('look')
def look_cmd(direction):
    _CONNECTION.look(direction)


@command_handler('quit')
def quit_cmd():
    global _RUNNING
    _RUNNING = False


def main():
    user = input('User Name: ')
    password = input('Password: ')

    if not _CONNECTION.login(user, password):
        return

    while _RUNNING:
        user_input = input("CMD: ").split(' ')
        cmd = user_input[0]
        if cmd in _COMMAND_HANDLERS:
            _COMMAND_HANDLERS[cmd](*user_input[1:])
        else:
            print("Invalid Command: {}".format(cmd))


if __name__ == '__main__':
    main()
