from flask import Flask
from flask_spyne import Spyne

from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument

from spyne.model.primitive import Unicode, Integer, Boolean, Float, String
from spyne.model.complex import Iterable, ComplexModel,Array
from spyne.model.primitive import DateTime,Date
from spyne.error import Fault

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


@app.errorhandler(Exception)
def handle_error(e):
    error_response = ErrorResponse()

    if isinstance(e, Exception):
        error_response.Error = "NOK: " + str(e)
        print(e)
        print(traceback.format_exc())
        app.logger.error(e)
        app.logger.error(traceback.format_exc())

        return error_response

    if isinstance(e, Fault):
        error_response.Error = "NOK: " + e.faultcode + " " + e.faultstring
        app.logger.error(e)
        app.logger.error(traceback.format_exc())
        return error_response

spyne = Spyne(app)


"""
    Modelos de spyne utilizados para crear el WSDL y manejar los requests y responses
"""


class AV(ComplexModel):

    key = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    value = Integer(min_occurs=1, max_occurs=1, nillable=False)


class Connection(ComplexModel):

    Index = Integer(min_occurs=0, max_occurs=1, nillable=True)
    flightNumber = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    airline = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    airlineIATA = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    flightNumber = Unicode(min_occurs=0, max_occurs=1, nillable=True)

    from_ = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    fromAirport = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    fromAirportIATA = Unicode(min_occurs=0, max_occurs=1, nillable=True)

    to = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    toAirport = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    toAirportIATA = Unicode(min_occurs=0, max_occurs=1, nillable=False)

    arrivalDateTime = DateTime(min_occurs=0, max_occurs=1, nillable=True)
    departureDatetime = DateTime(min_occurs=0, max_occurs=1, nillable=False)

    AV = Array(AV.customize(nillable=True))
    map = Unicode(min_occurs=0, max_occurs=1, nillable=False)


class Fare(ComplexModel):

    type = Unicode(min_occurs=1, max_occurs=1, nillable=True)
    fare_class = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    fare_name = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    fare_price = Float(min_occurs=0, max_occurs=1, nillable=True)
    currency = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    exchange_rate = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    fare_book = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    AV = Array(AV.customize(nillable=True))
    rules = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    return_ = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    connection = Unicode(min_occurs=0, max_occurs=1, nillable=True)


class Auth(ComplexModel):

    session = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    gcp = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    userId = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    userName = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    user = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    password = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    ip = Unicode(min_occurs=1, max_occurs=1, nillable=True)


class Flight(ComplexModel):

    __namespace__ = 'testing'
    Index = Integer(min_occurs=0, max_occurs=1, nillable=True)
    flightNumber = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    airline = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    airlineIATA = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    flightNumber = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    nChild = Integer(min_occurs=0, max_occurs=1, nillable=True)
    nInfant = Integer(min_occurs=0, max_occurs=1, nillable=True)
    arrivalDateTime = Unicode(min_occurs=0, max_occurs=1, nillable=True)

    from_ = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    to = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    departureDatetime = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    nAdult = Integer(min_occurs=0, max_occurs=1, nillable=False)
    AV = Array(AV.customize(nillable=True))
    LConnections = Array(Connection.customize(nillable=True))
    LFares = Array(Fare.customize(nillable=True))

    validReturns = Array(Unicode(min_occurs=0, max_occurs=1, nillable=False))
    type = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    return_ = Boolean(min_occurs=0, max_occurs=1, nillable=False)
    schedule = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    range = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    info = Unicode(min_occurs=0, max_occurs=1, nillable=False)

#  Clase que representa el input de GetFlights
class GetFlights(ComplexModel):

    auth = Auth(min_occurs=1, max_occurs=1, nillable=False)
    flight = Flight(min_occurs=1, max_occurs=1, nillable=False)

#  Clase que representa el output de GetFlights
class GetFlightsResponse(ComplexModel):

    Error = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    Flights = Array(Flight.customize(min_occurs=1, max_occurs=1, nillable=True))


class Region(ComplexModel):
    __namespace__ = 'get_destinations'
    id = Integer(min_occurs=1, max_occurs=1, nillable=False)
    name = Unicode(min_occurs=1, max_occurs=1, nillable=False)

class Country(ComplexModel):
    __namespace__ = 'get_destinations'
    id = Integer(min_occurs=1, max_occurs=1, nillable=False)
    code = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    name = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    name_spanish = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    continent = Unicode(min_occurs=1, max_occurs=1, nillable=False)

class Airport(ComplexModel):
    __namespace__ = 'get_destinations'
    id = Integer(min_occurs=1, max_occurs=1, nillable=False)
    code = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    name = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    international = Boolean(min_occurs=1, max_occurs=1, nillable=False)
    airport = Integer(min_occurs=1, max_occurs=1, nillable=False)

class Data(ComplexModel):
    __namespace__ = 'get_destinations'
    id = Integer(min_occurs=1, max_occurs=1, nillable=False)
    region = Region(min_occurs=1, max_occurs=1, nillable=True)
    country = Country(min_occurs=1, max_occurs=1, nillable=True)
    airports = Array(Airport.customize(min_occurs=1, max_occurs=1, nillable=True))
    code = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    name = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    pais = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    location = Unicode(min_occurs=1, max_occurs=1, nillable=False)

#clase que representa el response de getDestinations
class GetDestinationResponse(ComplexModel):
    Error = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    Data = Array(Data.customize(min_occurs=1, max_occurs=1, nillable=True))

# Clase que representa un Error
class ErrorResponse(ComplexModel):
    Error = Unicode(min_occurs=1, max_occurs=1, nillable=False)

class GetFlightService(spyne.Service):

    __service_url_path__ = '/test/get/flight'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = out_protocol = Soap11()

    @spyne.srpc(Auth, Flight,  _returns=GetFlightsResponse)
    def get_flights(auth, flight):

        request_json = generate_json_request_get_flights(auth, flight)

        headers = {'Content-type': 'application/json'}
        response_json = requests.post('http://localhost:5000/temp/get/flight', data=request_json, headers=headers)
        response_json = json.loads(response_json.text)

        get_flights_response = generate_get_flights_response(response_json)

        return get_flights_response

class GetDestinationService(spyne.Service):

    __service_url_path__ = '/get/destinations'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = out_protocol = Soap11()

    @spyne.srpc(String, _returns=GetDestinationResponse)
    def get_destinations(city):

        url = 'http://localhost:5000/get/destinations?city='+city

        headers = {'Content-type': 'application/json'}
        response_json = requests.get(url, headers=headers)
        response_json = json.loads(response_json.text)

        get_destination_response = generate_get_destinations_response(response_json)

        return get_destination_response

def generate_get_destinations_response(response_json):

    """
    "data": [
        {
            "id": 151,
            "region_id": {
                "id": 1,
                "name": "Default"
            },
            "country_id": {
                "id": 11,
                "code": "AR",
                "name": "ARGENTINA",
                "name_spanish": "ARGENTINA",
                "continent": "South America"
            },
            "airports": [
                {
                    "id": 2293,
                    "code": "EZE",
                    "name": "Ministro Pistarini",
                    "international": 0,
                    "airport": 1
                }
            ],
            "code": "EZE",
            "name": "Buenos Aires",
            "pais": "ARGENTINA",
            "location": "Ministro Pistarini"
        }
    ],

    :param response_json:
    :return:
    """

    datas = []

    get_destination_response = GetDestinationResponse()
    get_destination_response.Error = response_json["error"]

    if response_json["error"] == "OK":
        #  Por cada data recibidovoy a hacer la transformacion
        for d in response_json["data"]:

            new_data = Data()
            new_data.id = int(d["id"])
            new_data.code = d["code"]
            new_data.name = d["name"]
            new_data.pais = d["pais"]
            new_data.location = d["location"]

            #TODO

            datas.append(new_data)

        get_destination_response.Data = datas

    else:
        error_response = ErrorResponse()
        error_response.Error = response_json["error"]

    return get_destination_response

def generate_get_flights_response(response_json):

    flights = []

    get_flights_response = GetFlightsResponse()
    get_flights_response.Error = response_json["error"]

    if response_json["error"] == "OK":
        #  Por cada flight recibido, voy a recorrer tambien sus conexiones y fares y agregarlas a la respuesta
        for f in response_json["flights"]:
            f = json.dumps(f)
            print(f)
            new_flight = Flight()
            new_flight.from_ = f["from"]
            new_flight.to = f["to"]
            new_flight.airlineIATA = f["airlineIATA"]
            new_flight.airline = f["airline"]
            new_flight.flightNumber = f["flightNumber"]
            new_flight.range = f["range"]
            new_flight.arrivalDateTime = f["arrivalDateTime"]
            new_flight.departureDatetime = f.get("departureDateTime", "")
            new_flight.nAdult = f["nAdult"]
            new_flight.nChild = f["nChild"]
            new_flight.nInfant = f["nInfant"]
            new_flight.Index = int(f["Index"])
            new_flight.type = f["type"]
            new_flight.schedule = f["schedule"]
            new_flight.info = f["info"]
            new_flight.return_ = f["return"]
            new_flight.AV = f["AV"]
            new_flight.LConnections = []
            new_flight.LFares = []

            for c in f["LConnections"]:
                new_connection = Connection()
                new_connection.airline = c["airline"]
                new_connection.airlineIATA = c["airlineIATA"]
                new_connection.from_ = c["from"]
                new_connection.fromAirport = c["fromAiport"]
                new_connection.fromAirportIATA = c["fromAirportIATA"]
                new_connection.to = c["to"]
                new_connection.toAirport = c["toAirport"]
                new_connection.toAirportIATA = c["toAirpottIATA"]  # TODO corregir SOAP
                new_connection.flightNumber = c["flightNumber"]
                new_connection.map = c["map"]
                new_connection.departureDatetime = datetime.datetime.strptime(c["departureDatetime"],
                                                                              "%Y-%m-%dT%H:%M:%S")
                new_connection.arrivalDateTime = datetime.datetime.strptime(c["arrivalDateTime"],
                                                                            "%Y-%m-%dT%H:%M:%S")
                # new_connection.AV = c["AV"] TODO agregar AV a estructuras

                new_flight.LConnections.append(new_connection)

            for flare in f["LFares"]:
                new_fare = Fare()
                new_fare.type = flare["type"]
                new_fare.fare_name = flare["fare_name"]
                new_fare.fare_price = flare["fare_price"]
                new_fare.currency = flare["currency"]
                new_fare.exchange_rate = flare["exchange_rate"]
                new_fare.fare_book = flare["fare_book"]
                new_fare.rules = flare["rules"]
                new_fare.return_ = flare["return_"]
                new_fare.connection = flare["connection"]


                new_flight.LFares.append(new_fare)

            flights.append(new_flight)

        get_flights_response.Flights = flights

    else:
        error_response = ErrorResponse()
        error_response.Error = response_json["error"]

    return get_flights_response


def generate_json_request_get_flights(auth, flight):

    json_av = []
    if flight.AV is not None:
        for av in flight.AV:
            json_av.append({
                'key': av.key,
                'value': av.value
            })

    data_request = {
        "Auth": {
            "session": auth.session,
            "gcp": auth.gcp,
            "user": auth.user,
            "password": auth.password,
            "userId": auth.userId,
            "userName": auth.userName,
            "ip": auth.ip
        }, "request": {
            "carrier": "ecojet",
            "carrierName": "",
            "action": ""
        }, "flight": {
                "index": flight.Index,
                "flightNumber": flight.flightNumber,
                "airline": flight.airline,
                "airlineIATA": flight.airlineIATA,
                "from": flight.from_,
                "to": flight.to,
                "departureDatetime": flight.departureDatetime,
                "arrivalDatetime": flight.arrivalDateTime,
                "lConnections": flight.LConnections,
                "lFares": flight.LFares,
                "validReturns": flight.validReturns,
                "nAdult": flight.nAdult,
                "AV": json_av,
                "type": flight.type,
                "return": flight.return_,
                "lAction": "",
                "schedule": flight.schedule,
                "range": flight.range,
                "info": flight.info

        }
    }

    return json.dumps(data_request)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


