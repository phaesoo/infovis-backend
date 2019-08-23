from flask import Flask, Blueprint

from app.api.restplus import api
from app.utils.log import init_logger


init_logger(__name__)
app = Flask(__name__)

# https://flask-restplus.readthedocs.io/en/stable/parsing.html
app.config["BUNDLE_ERRORS"] = True


if app.config["DEBUG"]:
    app.config.from_pyfile("./configs/dev.py")
else:
    raise NotImplementedError


def initialize_app(flask_app):
    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api.init_app(blueprint)
    flask_app.register_blueprint(blueprint)

    # add namespaces

initialize_app(app)