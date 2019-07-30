from flask import Flask, request, jsonify
from os import path
from .settings import ProdConfig
from .exceptions import InvalidUsage
from image import index
from gazo import commands, extensions


def create_app(config=ProdConfig):
    app = Flask(__name__, static_url_path=config.IMAGE_FILES_DIR)
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    print(app.config['ENV'])
    register_blueprints(app)
    register_commands(app)
    register_extensions(app)
    register_errorhandlers(app)
    return app

def register_blueprints(app):
    app.register_blueprint(index.image)

def register_commands(app):
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.clean)

def register_extensions(app):
    extensions.redis.init_app(app)

def register_errorhandlers(app):
    def errorhandler(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)