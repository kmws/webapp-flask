from enum import Enum

from flask import jsonify

from tools.config_properties import get_config


class CustomError(Exception):
    def __init__(self, error_enum, status_code=None, payload=None):
        Exception.__init__(self)
        self.error_enum = error_enum
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['errorKey'] = self.error_enum.key
        rv['errorMessage'] = self.error_enum.value[get_config().get_language() or '']
        return rv


def register_custom_errors(app):
    @app.errorhandler(CustomError)
    def specify_auth_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


class Error(Enum):
    #AUTH
    AUTH_LOGIN_NOT_VALID_DATA_ERROR = {
        'eng': 'Entered login or password is not valid.'
    }
    AUTH_LOGIN_USER_NOT_FOUND_ERROR = {
        'eng': 'User with given email is not registered into service.'
    }
    AUTH_LOGIN_USER_NOT_ACTIVATED = {
        'eng': 'User with given email is not activated.'
    }
    AUTH_LOGIN_WRONG_PASSWORD = {
        'eng': 'Wrong password.'
    }

    #USER
    USER_ADD_ERROR = {
        'eng': 'There was a problem during'
    }

