# from flask_api import FlaskAPI
# from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

from flask import Flask
from flask_spyne import Spyne
from model import models

from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument
from spyne.error import Fault

import logging
from logging.handlers import RotatingFileHandler
import traceback
from instance import config

import json
import requests
import datetime

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, backref, sessionmaker

from werkzeug.exceptions import HTTPException
import logging
import traceback
from logging.handlers import RotatingFileHandler


from instance.config import app_config

"""Inicializo un ORM en el caso de que se necesite posteriormente"""
# db = SQLAlchemy()

def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#   db.init_app(app)
    set_log(app)
    spyne = Spyne(app)

    class flightSOAP(spyne.Service):
        __service_url_path__ = '/cnet/flight'
        __in_protocol__ = Soap11(validator='soft')
        __out_protocol__ = Soap11()

        @spyne.srpc(models.GetFlights, _in_message_name="getFlightsRequest",
                    _returns=models.GetFlightsResponse,
                    _body_style='bare')
        def getFlights(GetFlightsRequest):
            request_generator = models.RequestGenerator()
            respone_generator = models.ResponseGenerator()

            request_json = request_generator.generate_json_request_get_flights(GetFlightsRequest)
            print(config.Config.HOST_GDS_REST_API + 'temp/get/flight')
            headers = {'Content-type': 'application/json'}
            response_json = requests.post(config.Config.HOST_GDS_REST_API + 'temp/get/flight', data=request_json, headers=headers)
            response_json = json.loads(response_json.text)

            get_flights_response = respone_generator.generate_get_flights_response(response_json)

            return get_flights_response

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 200
        if isinstance(e, HTTPException):
            code = e.code
            app.logger.error(e)
            print(e)

        print(e)
        print(traceback.format_exc())

    return app

def set_log(app):
    file_handler = RotatingFileHandler('error.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    return app

