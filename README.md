# Transit∿

A realtime LED display connected to a Raspberry Pi that has arrival
times for the most frequently used transit stop you use at your home.

I'll be using Python 3, Flask 0.12.2, and my Raspberry Pi.

You can see a live version of this app on heroku:

[Transit ∿](https://transit-sign.herokuapp.com/)


To start the application in your local dev environment:

- python3 -m venv venv
- virtualenv -p python3 venv
- source venv/bin/activate
- pip3 install -r requirements.txt
- export FLASK_APP=transit-sign.py
- export FLASK_DEBUG=1
- flask db upgrade
- flask run

To run the tests:

- python tests.py
