from os.path import expanduser

import flask
from flask import jsonify, Flask
from flask_cors import CORS

from config.config import config
from gmail_client import GmailClient


def create_app() -> Flask:
    app = Flask(__name__)
    app = add_config(app, config)
    app = add_cors_wrapper(app)

    @app.route('/ping/')
    def ping():
        return jsonify({
            'ping': 'pong',
        })

    @app.route('/items/')
    def items():
        return jsonify({
            'items': [
                {'id': 1, 'name': 'Apples', 'price': '$2'},
                {'id': 2, 'name': 'Peaches', 'price': '$5'}
            ]
        })

    return app


def add_config(app: Flask, config: dict) -> Flask:
    for k, v in config.items():
        app.config[k] = v
    return app


def add_cors_wrapper(app: Flask) -> Flask:
    CORS(
        app, supports_credentials=True, resources={r'.*': {'origins': app.config['cors']['origins']}},
        allow_headers=app.config['cors']['allow_headers'],
    )
    return app

app = create_app()    

home = expanduser("~")

app.gmail_client = GmailClient(home + '/config/cyborg/credentials.json')

@app.route('/')
def index():
    endpoints = {'endpoints':['emails','data','dates']}
    return flask.jsonify(endpoints)

@app.route('/emails/')
def emails():
    response = app.gmail_client.count_daily_emails()
    return flask.jsonify(response)

@app.route('/data/')
def data():
    """
    This is a test endpoint. To be removed after confirmation that data
    has been sent to the frontend.
    """
    response = {
	    "data":{
	        "x": [1,2,3,4,5],
	        "y": [1,2,3,4,5]
	    }
    }
    return flask.jsonify(response)  


# -----------------------------------------
# these dates are for testing purposes only
# -----------------------------------------

daily_emails = [{"date":"18-11-17","email_count":1,"pretty_date":"Today"},{"date":"18-11-16","email_count":1,"pretty_date":"Friday, 16th"},{"date":"18-11-15","email_count":3,"pretty_date":"Thursday, 15th"},{"date":"18-11-14","email_count":1,"pretty_date":"Wednesday, 14th"},{"date":"18-11-13","email_count":3,"pretty_date":"Tuesday, 13th"},{"date":"18-11-12","email_count":5,"pretty_date":"Monday, 12th"},{"date":"18-11-11","email_count":3,"pretty_date":"Sunday, 11th"},{"date":"18-11-10","email_count":2,"pretty_date":"Saturday, 10th"},{"date":"18-11-09","email_count":2,"pretty_date":"Friday, 9th"},{"date":"18-11-08","email_count":3,"pretty_date":"Thursday, 8th"},{"date":"18-11-07","email_count":4,"pretty_date":"Wednesday, 7th"},{"date":"18-11-06","email_count":3,"pretty_date":"Tuesday, 6th"},{"date":"18-11-05","email_count":6,"pretty_date":"Monday, 5th"},{"date":"18-11-04","email_count":1,"pretty_date":"Sunday, 4th"}]
# -----------------------------------------

@app.route('/dates/')
def dates():
    """
    This is a test endpoint. To be removed after confirmation that data
    has been sent to the frontend.
    """
    response = {'daily_emails':daily_emails}
    
    return flask.jsonify(response)        

if __name__ == '__main__':
    app.run()
