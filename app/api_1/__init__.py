from http.client import HTTPException

from flask_restful import reqparse
from flask import request
from app import app
from app.conf.app_config import Configure
from app.lib.APIException import ApiException
from app.lib.Wus_Response import return_error
from app.lib.constant import UserConstant, defult
from app.util.encryption_util import Encryption


@app.before_request
def verify_token():
    if request.path not in Configure.white_token:
        token = request.headers.get("Authorization")[7:] if request.headers.get("Authorization") else ""
        c_data = Encryption.jwt_decode(token)
        if not token or not c_data:
            return return_error(*UserConstant.TOKEN_ERROR)
        else:
            request.ider = c_data


@app.errorhandler(ApiException)
def handle_invalid_usage(error):
    app.logger.exception('error 500: %s', error)
    if isinstance(error, HTTPException):
        return ApiException(*defult).to_dict()
    return error.to_dict()


def args_parse(schemy):
    def wrapps(func):

        def inner(*args, **kwargs):
            reparse = reqparse.RequestParser()

            for key, sc in schemy.items():
                reparse.add_argument(key, **sc)
            for k, y in reparse.parse_args().items():
                kwargs[k] = y
            return func(*args, **kwargs)

        return inner

    return wrapps


def error_vail():
    def wrapps(func):

        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return True
            except Exception as e:
                return False

        return inner

    return wrapps
