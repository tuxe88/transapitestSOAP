from flask import Flask
from flask_spyne import Spyne

from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument

from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable, ComplexModel
from spyne.model.primitive import DateTime

import logging

h = logging.StreamHandler()
rl = logging.getLogger()
rl.setLevel(logging.DEBUG)
rl.addHandler(h)

app = Flask(__name__)

spyne = Spyne(app)

class GetFlightsRequest(ComplexModel):
    __namespace__ = 'testing'
    Index = Integer(min_occurs=0, max_occurs=1, nillable=True)
    flightNumber = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    Index = Integer(min_occurs=0, max_occurs=1, nillable=True)
    flightNumber = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    airline = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    airlineIATA = Unicode(min_occurs=0, max_occurs=1, nillable=True)
    nChild = Integer(min_occurs=0, max_occurs=1, nillable=True)
    nInfant = Integer(min_occurs=0, max_occurs=1, nillable=True)
    arrivalDateTime = DateTime(min_occurs=0, max_occurs=1, nillable=True)

    from_ = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    to = Unicode(min_occurs=0, max_occurs=1, nillable=False)
    departureDatetime = DateTime(min_occurs=0, max_occurs=1, nillable=False)
    nAdult = Integer(min_occurs=0, max_occurs=1, nillable=False)

    LConnections = []
    LFares = []
    validReturns = ""
    AV = ""
    type = ""
    return_ = ""
    schedule = ""
    range = ""
    info = ""

class GetFlightService(spyne.Service):
    __service_url_path__ = '/test/get/flight'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = JsonDocument(ignore_wrappers=True)

    @spyne.srpc(Integer, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode,
                Unicode, Unicode, DateTime, DateTime,  _returns=GetFlightsRequest)

    def get_flights(index, flight_number, airline, airlineIATA, from_, to, nAdult, nChild, nInfant, departureDatetime,
                    arrivalDatetime):

        return GetFlightsRequest(Index=index, flightNumber=flight_number, airline=airline, airlineIATA=airlineIATA,
                                 from_=from_, to=to, nAdult = nAdult ,nChild = nChild, nInfant = nInfant,
                                 departureDatetime = departureDatetime, arrivalDatetime = arrivalDatetime)


if __name__ == '__main__':
    app.run(host='0.0.0.0')