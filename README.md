# gdsAPI SOAP

Instrucciones para crear el entorno de desarrollo en windows

### Prerequisitos
* python 2.7 (actualmnente utilizando 2.7.15)
* Tener python2 agregado en PATH
* En caso de tener ambas versiones instaladas, lo ideal es cambiar el nombre de los ejecutables a python2 y python3 
(Así pueden convivir ambos y ejecutarse cada uno cuando sea necesario)

    https://datascience.com.co/how-to-install-python-2-7-and-3-6-in-windows-10-add-python-path-281e7eae62a

## Deployment

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

Xml utlilizado para testear
```xml
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="tns" xmlns:soap="soap" xmlns:tes="testing">
       <soapenv:Header/>
       <soapenv:Body>
          <tns:get_flights>
             <!--Optional:-->
             <tns:auth>
                <!--Optional:-->
                <soap:userName></soap:userName>
                <soap:ip></soap:ip>
                <soap:userId></soap:userId>
                <soap:gcp></soap:gcp>
                <soap:session></soap:session>
                <!--Optional:-->
                <soap:user></soap:user>
                <!--Optional:-->
                <soap:password></soap:password>
             </tns:auth>
             <!--Optional:-->
             <tns:flight>
                <!--Optional:-->
                <tes:Index>1</tes:Index>
                <!--Optional:-->
                <tes:airlineIATA></tes:airlineIATA>
                <!--Optional:-->
                <tes:arrivalDateTime></tes:arrivalDateTime>
                <!--Optional:-->
                <tes:validReturns>
                   <!--Zero or more repetitions:-->
                   <tns:string></tns:string>
                </tes:validReturns>
                <!--Optional:-->
                <tes:nChild>0</tes:nChild>
                <!--Optional:-->
                <tes:return_>1</tes:return_>
                <!--Optional:-->
                <tes:to>MEX</tes:to>
                <!--Optional:-->
                <tes:nAdult>1</tes:nAdult>
                <!--Optional:-->
                <tes:from_>EZE</tes:from_>
                <!--Optional:-->
                <tes:type></tes:type>
                <!--Optional:-->
                <tes:nInfant>0</tes:nInfant>
                <!--Optional:-->
                <tes:schedule></tes:schedule>
                <!--Optional:-->
                <tes:AV>
                   <!--Zero or more repetitions:-->
                   <soap:AV>
                      <soap:value>1</soap:value>
                      <soap:key>cabinClass</soap:key>
                   </soap:AV>
                </tes:AV>
                <!--Optional:-->
                <tes:departureDatetime>20/10/2018</tes:departureDatetime>
                <!--Optional:-->
                <tes:info></tes:info>
                <!--Optional:-->
                <tes:flightNumber></tes:flightNumber>
                <!--Optional:-->
                <tes:range></tes:range>
                <!--Optional:-->
                <tes:airline></tes:airline>
             </tns:flight>
          </tns:get_flights>
       </soapenv:Body>
    </soapenv:Envelope>
```


## Realizado con

* [Flask](http://flask.pocoo.org/)
* [Spyne](http://spyne.io)
