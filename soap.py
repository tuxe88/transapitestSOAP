from flask import Flask
from flask_spyne import Spyne
import re

from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument


from spyne.model.primitive import Unicode, Integer, Boolean
from spyne.model.complex import Iterable, ComplexModel,Array
from spyne.model.primitive import DateTime

import json
import logging
import requests
import datetime

h = logging.StreamHandler()
rl = logging.getLogger()
rl.setLevel(logging.DEBUG)
rl.addHandler(h)

app = Flask(__name__)

spyne = Spyne(app)

class AV(ComplexModel):
    key = Integer(min_occurs=1, max_occurs=1, nillable=False)
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

    type = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    value = Integer(min_occurs=1, max_occurs=1, nillable=False)


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
    arrivalDateTime = DateTime(min_occurs=0, max_occurs=1, nillable=True)

    from_ = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    to = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    departureDatetime = DateTime(min_occurs=0, max_occurs=1, nillable=False)
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


class GetFlights(ComplexModel):

    auth = Auth(min_occurs=1, max_occurs=1, nillable=False)
    flight = Flight(min_occurs=1, max_occurs=1, nillable=False)


class GetFlightsResponse(ComplexModel):

    Error = Unicode(min_occurs=1, max_occurs=1, nillable=False)
    Flights = Array(Flight.customize(min_occurs=1, max_occurs=1, nillable=True))


class GetFlightService(spyne.Service):
    __service_url_path__ = '/test/get/flight'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = out_protocol=Soap11()

    @spyne.srpc(Auth, Flight,  _returns=GetFlightsResponse)
    def get_flights(auth, flight):

        request_json = generate_json_request_get_flights(auth, flight)

        headers = {'Content-type': 'application/json'}
        response_json = requests.post('http://localhost:5000/temp/get/flight', data=request_json, headers=headers)

        response_json = json.loads(response_json.text)

        flights = []

        get_flights_response = GetFlightsResponse()
        get_flights_response.Error = response_json["error"]

        for f in response_json["flights"]:
            new_flight = Flight()

            new_flight.departureDatetime = datetime.strptime(f["departureDatetime"],"'%Y-%d-%bT%I:%M%p'")
            new_flight.departureDatetime = datetime.strptime(f["arrivalDateTime"], "'%Y-%d-%bT%I:%M%p'")
            new_flight.from_ = f["from"]
            new_flight.to = f["to"]
            new_flight.airlineIATA = f["airlineIATA"]
            new_flight.airline = f["airline"]
            new_flight.flightNumber = f["flightNumber"]
            new_flight.range = f["range"]

            new_flight.type = f["type"]
            new_flight.schedule = f["schedule"]
            new_flight.info = f["info"]
            new_flight.return_ = f["return"]

            # new_flight.validReturns = f["validReturns"]
            # new_flight.Index = f["Index"]
            #
            """
            new_flight.nAdult = f["nAdult"]
            new_flight.nChild = f["nChild"]
            new_flight.nInfant = f["nInfant"]
            
            """

            flights.append(new_flight)


        get_flights_response.Flights = flights
        return get_flights_response


def generate_json_request_get_flights(auth, flight):

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
            "index": {
                "flightNumber": flight.flightNumber,
                "airline": flight.airline,
                "airlineIATA": flight.airlineIATA,
                "from": flight.from_,
                "to": flight.to,
                "departureDatetime": str(flight.departureDatetime),
                "arrivalDatetime": str(flight.arrivalDateTime),
                "lConnections": flight.LConnections,
                "lFares": flight.LFares,
                "validReturns": flight.validReturns,
                "nAdult": flight.nAdult,
                "AV": [
                    {
                        "key": "nSenior",
                        "value": "0"
                    },
                    {
                        "key": "cabinClass",
                        "value": 0
                    }
                ],
                "type": flight.type,
                "return": flight.return_,
                "lAction": "",
                "schedule": flight.schedule,
                "range": flight.range,
                "info": flight.info
            }
        }
    }

    return json.dumps(data_request)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
