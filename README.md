# gdsAPI SOAP

Instrucciones para crear el entorno de desarrollo en windows

### Prerequisitos
* python 2.7 (actualmnente utilizando 2.7.15)
* Tener python2 agregado en PATH
* En caso de tener ambas versiones instaladas, lo ideal es cambiar el nombre de los ejecutables a python2 y python3 
(Así pueden convivir ambos y ejecutarse cada uno cuando sea necesario)

    https://datascience.com.co/how-to-install-python-2-7-and-3-6-in-windows-10-add-python-path-281e7eae62a

## Deployment Windows

Activo el virtualenv
```
CARPETA_DEL_PROYECTO\venv\Scripts\activate
```
Instalo los requerimientos
```
pip install -r requirements.txt
```
Seteo las variables de entorno
```
set FLASK_APP=soap.py
```

```
set FLASK_ENV=development
```
Corro el server (En este caso en el puerto 5010, porque la api REST utiliza el 5000)
```
flask run --host=0.0.0.0 --port=5010
```
WSDL generado por spyne
```
http://127.0.0.1:5010/test/get/flight?wsdl
```


## Deployment Linux

Se crea el virtualenv
```
virtualenv -p /usr/bin/python2.7 CARPETA_DEL_PROYECTO\venv
```
Activo el virtualenv
```
virtualenv CARPETA_DEL_PROYECTO\venv\Scripts\activate
```
Instalo los requerimientos
```
pip install -r requirements.txt
```
Seteo las variables de entorno
```
export FLASK_APP=soap.py
```

```
export FLASK_ENV=development
```
Corro el server (En este caso en el puerto 5010, porque la api REST utiliza el 5000)
```
flask run --host=0.0.0.0 --port=5010
```
WSDL generado por spyne
```
http://127.0.0.1:5010/test/get/flight?wsdl
```

## Realizado con

* [Flask](http://flask.pocoo.org/)
* [Spyne](http://spyne.io)