from flask import Flask
from flask_spyne import Spyne

from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument

from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable, ComplexModel,Array
from spyne.model.primitive import DateTime

import logging

h = logging.StreamHandler()
rl = logging.getLogger()
rl.setLevel(logging.DEBUG)
rl.addHandler(h)

app = Flask(__name__)

spyne = Spyne(app)


class AV(ComplexModel):
    key = Integer(min_occurs=1, max_occurs=1, nillable=False)
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

    LConnections = []
    LFares = []
    validReturns = ""
    type = ""
    return_ = ""
    schedule = ""
    range = ""
    info = ""


class GetFlights(ComplexModel):

    auth = Auth(min_occurs=1, max_occurs=1, nillable=False)
    flight = Flight(min_occurs=1, max_occurs=1, nillable=False)

class GetFlightsResponse(ComplexModel):

    auth = Auth(min_occurs=1, max_occurs=1, nillable=False)
    flights = Array(Flight.customize(min_occurs=1, max_occurs=1, nillable=False))


class GetFlightService(spyne.Service):
    __service_url_path__ = '/test/get/flight'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = JsonDocument(ignore_wrappers=True)

    @spyne.srpc(Auth, Flight,  _returns=GetFlights)
    def get_flights(Auth, Flight):

        return GetFlights(Auth,Flight)

class GetFlightResponseService(spyne.Service):
    __service_url_path__ = '/test/get/flight'
    __in_protocol__ = JsonDocument(ignore_wrappers=True)
    __out_protocol__ = Soap11(validator='lxml')

    @spyne.srpc(Auth, Flight,  _returns=GetFlightsResponse)
    def get_flights(Auth, Flight):

        return GetFlights(Auth,Flight)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
