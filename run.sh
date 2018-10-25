source venv/bin/activate
export FLASK_APP=soap
export FLASK_ENV=development
export API_SOAP_PORT=5010
export API_REST_PORT=5000
export HOST_GDSAPI=http://mozart.microblet.com:${API_REST_PORT}/
nohup flask run --host=0.0.0.0 --port=${API_SOAP_PORT} &
deactivate
