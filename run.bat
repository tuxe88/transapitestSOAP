call venv\Scripts\activate
call set FLASK_APP=soap.py
call set FLASK_ENV=development
call flask run --host=0.0.0.0 --port=5010