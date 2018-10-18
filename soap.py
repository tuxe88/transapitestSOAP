from flask import Flask
from flask_spyne import Spyne

from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument
from spyne.util.odict import odict
from spyne.model.complex import ComplexModelBase

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

"""clase AV"""
od = odict()
od['key'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['value'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
AV = ComplexModelBase.produce('str', 'AV', od)


"""
<str:map>
                  <!--1 or more repetitions:-->
                  <str:rows>
                     <!--1 or more repetitions:-->
                     <str:seats>
                        <str:seat>?</str:seat>
                        <str:seatCode>?</str:seatCode>
                        <str:availability>?</str:availability>
                     </str:seats>
                  </str:rows>
                  <str:numRows>?</str:numRows>
                  <str:numCols>?</str:numCols>
                  <str:numSeats>?</str:numSeats>
                  <!--Optional:-->
                  <str:name>?</str:name>
               </str:map>
"""

od = odict()
od['seat'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['seatCode'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['availability'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
Seats = ComplexModelBase.produce('str', 'seats', od)

od = odict()
od['rows'] = Array(Seats.customize(min_occurs=1, nillable=False))
od['numRows'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['numCols'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['numSeats'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['name'] = Unicode(min_occurs=1, max_occurs=1, nillable=True)
Map = ComplexModelBase.produce('str', 'map', od)

"""clase Connection"""
od = odict()
od['index'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['airline'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['airlineIATA'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['from'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['fromAirport'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['fromAirportIATA'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['to'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['toAirport'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['toAirportIATA'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['departureDatetime'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['arrivalDatetime'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['flightNumber'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['map'] = Map.customize(min_occurs=0, max_occurs='unbound', nillable=True)
od['AV'] = Array(AV.customize(min_occurs=0, max_occurs=1, nillable=False))
Connection = ComplexModelBase.produce('str', 'lConnections', od)

"""clase ruless""" #TODO revisar esto con nico
od = odict()
od['key'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['value'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
RulesChild = ComplexModelBase.produce('str', 'ruless', od)

"""clase rules"""
od = odict()
od['ruleName'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['rules'] = Array(RulesChild.customize(min_occurs=0, max_occurs='unbounded', nillable=False))
Rules = ComplexModelBase.produce('str', 'rules', od)

"""clase Fare"""
od = odict()
od['type'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['fareClass'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['fareName'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['farePrice'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['currency'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['exchangeRate'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['fareBook'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['AV'] = AV.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['rules'] = Rules.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['return'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['connection'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
Fare = ComplexModelBase.produce('str', 'lFares', od)

"""clase Auth"""
od = odict()
od['session'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['gcp'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['userId'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['userName'] = Integer(min_occurs=1, max_occurs=1, nillable=True)
od['user'] = Integer(min_occurs=1, max_occurs=1, nillable=True)
od['password'] = Integer(min_occurs=1, max_occurs=1, nillable=True)
od['ip'] = Integer(min_occurs=1, max_occurs=1, nillable=True)
Auth = ComplexModelBase.produce('str', 'auth', od)

"""clase schedule"""
od = odict()
od['name'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['start'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
od['end'] = Integer(min_occurs=1, max_occurs=1, nillable=False)
Schedule = ComplexModelBase.produce('str', 'schedule', od)

"""clase flight"""
od = odict()
od['index'] = Integer(min_occurs=0, max_occurs=1, nillable=True)
od['flightNumber'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['airline'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['airlineIATA'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['from'] = Unicode(min_occurs=0, max_occurs=1, nillable=False)
od['to'] = Unicode(min_occurs=0, max_occurs=1, nillable=False)
od['departureDatetime'] = Unicode(min_occurs=0, max_occurs=1, nillable=False)
od['arrivalDatetime'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['lConnections'] = Connection.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['lFares'] = Fare.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['validReturns'] = Unicode(min_occurs=0, max_occurs='unbounded', nillable=True)
od['nAdult'] = Integer(min_occurs=0, max_occurs=1, nillable=False)
od['nChild'] = Integer(min_occurs=0, max_occurs=1, nillable=True)
od['nInfant'] = Integer(min_occurs=0, max_occurs=1, nillable=True)
od['AV'] = AV.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['type'] = Unicode(min_occurs=0, max_occurs=1, nillable=False)
od['return'] = Boolean(min_occurs=0, max_occurs=1, nillable=False)
od['schedule'] = Schedule.customize(min_occurs=0, max_occurs=1, nillable=True)
od['range'] = Unicode(min_occurs=0, max_occurs=1, nillable=False)
od['info'] = Unicode(min_occurs=0, max_occurs=1, nillable=False)

Flight = ComplexModelBase.produce('str', 'flight', od)

"""clase GetFlights"""
od = odict()
od['auth'] = Connection.customize(min_occurs=1, max_occurs=1, nillable=False)
od['flight'] = Flight.customize(min_occurs=1, max_occurs=1, nillable=False)

GetFlights = ComplexModelBase.produce('str', 'getFlights', od)

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

class flightSOAP(spyne.Service):

    __service_url_path__ = '/test/get/flight'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = out_protocol = Soap11()

    @spyne.srpc(Auth, Flight,  _returns=GetFlightsResponse)
    def getFlights(auth, flight):
        request_json = generate_json_request_get_flights(auth, flight)

        headers = {'Content-type': 'application/json'}
        response_json = requests.post('http://localhost:5000/temp/get/flight', data=request_json, headers=headers)
        response_json = json.loads(response_json.text)

        get_flights_response = generate_get_flights_response(response_json)

        return get_flights_response

    @spyne.srpc(String, _returns=GetDestinationResponse)
    def getDestinations(city):
        url = 'http://localhost:5000/get/destinations?city=' + city

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


