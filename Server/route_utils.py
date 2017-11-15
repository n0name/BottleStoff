from flask import make_response, jsonify, request


def ok(data):
    return make_response(jsonify(data), 200)


def error(message, error_code=400):
    return make_response(jsonify({"Error": message}), error_code)


def check_fields(request_json, *fields):
    for field in fields:
        if field not in request_json:
            return False
    return True


def required_fields(*fields):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if not request.json:
                return error("Non Json Input")

            if not check_fields(request.json, *fields):
                return error("invalid input")

            return function(*args, **kwargs)

        return wrapper

    return real_decorator
