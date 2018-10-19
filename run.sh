source venv/bin/activate
export FLASK_APP=soap
export FLASK_ENV=development
export HOST_GDSAPI=http://mozart.microblet.com/
nohup flask run --host=0.0.0.0 --port=5010 &
deactivate
