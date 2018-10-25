from spyne.model.complex import ComplexModelBase
from spyne.model.primitive import Unicode, Integer, Boolean, Float, String, AnyXml
from spyne.model.complex import Iterable, ComplexModel,Array
from spyne.model.primitive import DateTime,Date
import json
from parameters import *
from spyne.util.odict import odict

"""
    Modelos de spyne utilizados para crear el WSDL y manejar los requests y responses
"""


"""clase AV"""
od = odict()
od['key'] = Unicode(min_occurs=1, nillable=False)
od['value'] = Integer(min_occurs=1, max_occurs=1, nillable=True, default=0)
AV = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'AV', od)


od = odict()
od['seat'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['seatCode'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['availability'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
Seat = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'Seat', od)

od = odict()
od['seats'] = Seat.customize(min_occurs=1, max_occurs='unbounded', nillable=False)
Row = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'Row', od)

od = odict()
od['rows'] = Row.customize(min_occurs=1, max_occurs='unbounded', nillable=False)
od['numRows'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['numCols'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['numSeats'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['name'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
Map = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'Map', od)

"""clase Connection"""
od = odict()
od['index'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['airline'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['airlineIATA'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['from'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['fromAirport'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['fromAirportIATA'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['to'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['toAirport'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['toAirportIATA'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['departureDatetime'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['arrivalDatetime'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['flightNumber'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['map'] = Map.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['AV'] = AV.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
Connection = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'Connection', od)


"""clase rules"""
od = odict()
od['ruleName'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['rules'] = AV.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
FareRule = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'FareRule', od)

"""clase Fare"""
od = odict()
od['type'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['fareClass'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['fareName'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['farePrice'] = Float(min_occurs=1, max_occurs=1, nillable=False, default=0)
od['currency'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['exchangeRate'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['fareBook'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['AV'] = AV.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['rules'] = FareRule.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['return'] = Boolean(min_occurs=0, max_occurs=1, nillable=True, default=False)
od['connection'] = Boolean(min_occurs=0, max_occurs=1, nillable=True, default=0)
Fare = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'Fare', od)

"""clase Auth"""
od = odict()
od['session'] = Unicode(min_occurs=1, max_occurs=1, nillable=True, default='')
od['gcp'] = Unicode(min_occurs=1, max_occurs=1, nillable=True)
od['userId'] = Unicode(min_occurs=1, max_occurs=1, nillable=True)
od['userName'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['user'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['password'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['ip'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
Auth = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'Auth', od)

"""clase schedule"""
od = odict()
od['name'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['start'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['end'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
Schedule = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'Schedule', od)

"""clase flight"""
od = odict()
od['index'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['flightNumber'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['airline'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['airlineIATA'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['from'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['to'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['departureDatetime'] = Unicode(min_occurs=1, max_occurs=1, nillable=False)
od['arrivalDatetime'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['lConnections'] = Connection.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['lFares'] = Fare.customize(min_occurs=0, max_occurs='unbounded', nillable=True)
od['validReturns'] = Unicode(min_occurs=0, max_occurs='unbounded', nillable=True)
od['nAdult'] = Integer(min_occurs=1, max_occurs=1, nillable=False, default=0)
od['nChild'] = Integer(min_occurs=1, max_occurs=1, nillable=True, default=0)
od['nInfant'] = Integer(min_occurs=1, max_occurs=1, nillable=True, default=0)
od['AV'] = AV.customize(min_occurs=1, max_occurs='unbounded', nillable=True)
od['type'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['return'] = Boolean(min_occurs=0, max_occurs=1, nillable=False, default=False)
od['schedule'] = Schedule.customize(min_occurs=0, max_occurs=1, nillable=True)
od['range'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)
od['info'] = Unicode(min_occurs=0, max_occurs=1, nillable=True)

Flight = ComplexModelBase.produce(STRUCTURE_NAMESPACE, 'Flight', od)

"""clase getFlights"""
od = odict()
od['auth'] = Auth.customize(min_occurs=1, max_occurs=1, nillable=False)
od['flight'] = Flight.customize(min_occurs=1, max_occurs=1, nillable=False)

GetFlights = ComplexModelBase.produce(GLOBAL_NAMESPACE, 'GetFlights', od)

"""clase GetFlightsResponse"""
od = odict()
od['error'] = Unicode.customize(min_occurs=1, nillable=False)
od['flights'] = Flight.customize(min_occurs=0, max_occurs='unbounded', nillable=True)

GetFlightsResponse = ComplexModelBase.produce(GLOBAL_NAMESPACE, 'GetFlightsResponse', od)


class AttributeT:
    read_only = False

#Clase generada para burlar una restriccion de spyne
class TempT:
    Attributes = AttributeT()

class ResponseGenerator:

    def generate_get_flights_response(self, response_json):

        flights = []

        get_flights_response = GetFlightsResponse()
        get_flights_response.Error = response_json["error"]
        mTemp = TempT()

        if response_json["error"] == "OK":
            #  Por cada flight recibido, voy a recorrer tambien sus conexiones y fares y agregarlas a la respuesta
            for f in response_json["flights"]:
                # f = json.dumps(f)
                new_flight = Flight()
                new_flight._safe_set("from", f["from"], mTemp)
                new_flight.to = f["to"]
                new_flight.airlineIATA = f["airlineIATA"]
                new_flight.airline = f["airline"]
                new_flight.flightNumber = f["flightNumber"]
                new_flight.range = f["range"]
                new_flight.arrivalDatetime = f["arrivalDateTime"]
                new_flight.departureDatetime = f.get("departureDateTime", "")
                new_flight.nAdult = f["nAdult"]
                new_flight.nChild = f["nChild"]
                new_flight.nInfant = f["nInfant"]
                new_flight.index = str(f["Index"])
                new_flight.type = f["type"]
                new_flight.schedule = f["schedule"]
                new_flight.info = f["info"]
                new_flight._safe_set("return", f["return"], mTemp)
                new_flight.AV = f["AV"]
                new_flight.lConnections = []
                new_flight.lFares = []

                for c in f["LConnections"]:
                    new_connection = Connection()
                    new_connection.index = str(c["Index"])
                    new_connection.airline = c["airline"]
                    new_connection.airlineIATA = c["airlineIATA"]
                    new_connection._safe_set("from", c["from"], mTemp)
                    new_connection.fromAirport = c["fromAiport"]
                    new_connection.fromAirportIATA = c["fromAirportIATA"]
                    new_connection.to = c["to"]
                    new_connection.toAirport = c["toAirport"]
                    new_connection.toAirportIATA = c["toAirpottIATA"]  # TODO corregir SOAP
                    new_connection.flightNumber = c["flightNumber"]
                    new_connection.map = c["map"]
                    new_connection.departureDatetime = c["departureDatetime"]
                    new_connection.arrivalDateTime = c["arrivalDateTime"]
                    # new_connection.AV = c["AV"] TODO agregar AV a estructuras

                    new_flight.lConnections.append(new_connection)

                for flare in f["LFares"]:
                    new_fare = Fare()
                    new_fare.type = flare["type"]
                    new_fare.fare_name = flare["fare_name"]
                    new_fare.fare_price = flare["fare_price"]
                    new_fare.currency = flare["currency"]
                    new_fare.exchange_rate = flare["exchange_rate"]
                    new_fare.fare_book = flare["fare_book"]

                    new_fare.rules = flare["rules"]
                    new_fare._safe_set("return", flare.get("return", []), mTemp)
                    new_fare.connection = flare["connection"]

                    new_flight.lFares.append(new_fare)

                flights.append(new_flight)

            get_flights_response.flights = flights
            get_flights_response.error = "OK"

        else:
            get_flights_response = GetFlightsResponse()
            get_flights_response.error = response_json["error"]

        return get_flights_response


class RequestGenerator:

    def generate_json_request_get_flights(self, get_flights):

        auth = get_flights.auth
        flight = get_flights.flight

        json_av = []
        if flight.AV is not None:
            for av in flight.AV:
                if av is not None:
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
                "index": flight.index,
                "flightNumber": flight.flightNumber,
                "airline": flight.airline,
                "airlineIATA": flight.airlineIATA,
                "from": flight.as_dict()["from"],
                "to": flight.to,
                "departureDatetime": flight.departureDatetime,
                "arrivalDatetime": flight.arrivalDatetime,
                "lConnections": flight.lConnections,
                "lFares": flight.lFares,
                "validReturns": flight.validReturns,
                "nAdult": flight.nAdult,
                "AV": json_av,
                "type": flight.type,
                "return": flight.as_dict().get("return", []),
                "lAction": "",
                "schedule": "",
                "range": "",
                "info": ""

            }
            # Range, schedule e info son ignorados porque no se usan
        }

        return json.dumps(data_request)



"""

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
"""


"""
    @spyne.srpc(String, _returns=GetDestinationResponse)
    def getDestinations(city):
        url = 'http://localhost:5000/get/destinations?city=' + city

        headers = {'Content-type': 'application/json'}
        response_json = requests.get(url, headers=headers)
        response_json = json.loads(response_json.text)

        get_destination_response = generate_get_destinations_response(response_json)

        return get_destination_response
"""
"""

def generate_get_destinations_response(response_json):

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
    """
