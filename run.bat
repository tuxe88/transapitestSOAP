call venv\Scripts\activate
call set FLASK_APP=soap.py
call set FLASK_ENV=development
call set API_REST_PORT=5000
call set API_SOAP_PORT=5010
call set HOST_GDSAPI=http://127.0.0.1:%API_REST_PORT%/
call flask run --host=0.0.0.0 --port=%API_SOAP_PORT%