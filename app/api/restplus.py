import logging
from flask_restplus import Api
from flask import current_app as app
from app.define import status
from app.utils.response import error


logger = logging.getLogger(__name__)
api = Api(version="1.0.0", title="Information visualization")


@api.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occured."
    logger.exception(message)
    print ("=== Error: {}".format(e))

    if app.config.get("DEBUG", False):
        return error(e, status=status.ERROR_SERVER)
    else:
        return error(message, status=status.ERROR_SERVER)
