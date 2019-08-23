from flask import Flask, Blueprint

from app.api.restplus import api
from app.utils.log import init_logger
from app.utils.json_encoder import CustomJSONEncoder
from app.api.timeseries.endpoints import ns as ns_timeseries


init_logger(__name__)
app = Flask(__name__)

# https://flask-restplus.readthedocs.io/en/stable/parsing.html
app.config["BUNDLE_ERRORS"] = True


if app.config["DEBUG"]:
    app.config.from_pyfile("./configs/dev.py")
else:
    raise NotImplementedError


def initialize_app(flask_app):
    # register blueprint
    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api.init_app(blueprint)
    flask_app.register_blueprint(blueprint)

    # set custom encoder
    flask_app.json_encoder = CustomJSONEncoder

    # add namespaces
    api.add_namespace(ns_timeseries)


initialize_app(app)