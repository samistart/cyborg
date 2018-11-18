from flask import Flask, jsonify
from flask_cors import CORS

from config.config import config


def create_app() -> Flask:

    app = Flask(__name__)
    app = add_config(app, config)
    app = add_cors_wrapper(app)

    @app.route('/ping/')
    def ping():
        return jsonify({
            'ping': 'pong',
        })

    return app


def add_config(app: Flask, config: dict) -> Flask:
    for k,v in config.items():
        app.config[k] = v
    return app


def add_cors_wrapper(app: Flask) -> Flask:
    CORS(
        app, supports_credentials=True, resources={r'.*': {'origins': app.config['cors']['origins']}},
        allow_headers=app.config['cors']['allow_headers'],
    )
    return app
