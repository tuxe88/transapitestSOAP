# gdsAPI

Instrucciones para crear el entorno de desarrollo en windows

### Prerequisitos
* python 2.7 (actualmnente utilizando 2.7.15)
* Tener python agregado en PATH


```
pip install -r requirements.txt
```

## Deployment

```
set FLASK_APP=soap.py
```

set FLASK_ENV=development

```
flask run --host=0.0.0.0 --port=5010
```

```
http://127.0.0.1:5010/test/get/flight?wsdl
```


## Realizado con

* [Flask](http://flask.pocoo.org/)
