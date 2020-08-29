# Install required dependencies by running
# pip install -r requirements.txt
# Feel free to use a virtual environment
export FLASK_APP=wsgi:app
flask db init
flask db migrate
flask db upgrade
gunicorn -b 0.0.0.0:80 wsgi:app # flask run for development