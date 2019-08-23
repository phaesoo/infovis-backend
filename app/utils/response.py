from flask import jsonify, make_response

from app.define import status


def sucess(data, status=status.SUCESS_OK):
    return make_response(
        jsonify({
            "status": "success",
            "data": data
        }), status)


def error(msg, status=status.ERROR_BAD_REQUEST):
    return make_response(
        jsonify({
            "status": "error",
            "message": msg
        }), status)


