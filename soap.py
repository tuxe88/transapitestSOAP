from flask import Flask
from flask_spyne import Spyne
from model import models

from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument
from spyne.error import Fault
from parameters import *

import logging
from logging.handlers import RotatingFileHandler
import traceback

import json
import requests
import datetime

app = Flask(__name__)

file_handler = RotatingFileHandler('error.log', maxBytes=1024 * 1024 * 100, backupCount=20)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

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
        print(HOST_GDS_API+'temp/get/flight')
        headers = {'Content-type': 'application/json'}
        response_json = requests.post(HOST_GDS_API+'temp/get/flight', data=request_json, headers=headers)
        response_json = json.loads(response_json.text)

        get_flights_response = respone_generator.generate_get_flights_response(response_json)

        return get_flights_response

if __name__ == '__main__':
    app.run(host='0.0.0.0')


