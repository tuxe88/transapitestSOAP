import logging
from suds.client import Client as SudsClient
import requests

url = 'http://127.0.0.1:5010/cnet/flight?wsdl'
client = SudsClient(url=url, cache=None)
r = client.service.get_flights()
