import logging
from suds.client import Client as SudsClient
import requests

url = 'http://127.0.0.1:5000/test/get/flight?wsdl'
client = SudsClient(url=url, cache=None)
r = client.service.get_flights()
print(r)


"""

r = client.service.answer(str='some question')
print(r)

url = 'http://127.0.0.1:5000/json/anotherservice/echo'
params = {'str': 'olos', 'cnt': 10}
r = requests.get(url=url, params=params)
print(r.text)

url = 'http://127.0.0.1:5000/json/anotherservice/answer'
params = {'str': 'olos'}
r = requests.get(url=url, params=params)
print(r.text)


class SomeSoapServiceTwo(spyne.Service):
    __service_url_path__ = '/soap/someservicetwo'
    __target_namespace__ = 'custom_namespacetwo'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, Integer, _returns=Iterable(Unicode))
    def echo(str, cnt):
        for i in range(cnt):
            yield str

    @spyne.srpc(Unicode, _returns=AnswerServiceResponse)
    def answer(str):
        return AnswerServiceResponse(dummy_str='answer is', dummy_num=42)


class SomeJsonService(spyne.Service):
    __service_url_path__ = '/json/anotherservice'
    __in_protocol__ = HttpRpc(validator='soft')
    __out_protocol__ = JsonDocument(ignore_wrappers=True)

    @spyne.srpc(Unicode, Integer, _returns=Iterable(Unicode))
    def echo(str, cnt):
        for i in range(cnt):
            yield str

    @spyne.srpc(Unicode, _returns=AnswerServiceResponse)
    def answer(str):
        return AnswerServiceResponse(dummy_str='answer is', dummy_num=42)


"""
