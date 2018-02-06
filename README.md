# led-transit-sign

Micro Project to create a realtime lcd display connected to a Raspberry Pi that has arrival
times for the most frequently used transit stop I have at my apartment.

I'll be using Python 3, Flask 0.12.2, and my Raspberry Pi.


To start the application:

- python3 -m venv venv
- virtualenv -p python3 venv
- source venv/bin/activate
- pip3 install -r requirements.txt
- export FLASK_APP=lcd-transit-sign.py
- export FLASK_DEBUG=1
- flask run

To run the tests: