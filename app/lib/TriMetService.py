import urllib, xmltodict
# from app import app
from flask import current_app as app

class TriMetService():

  def __init__(self, locations):
    # must be list of locations
    self.locations = locations
    self.tri_met_app_id = app.config['TRI_MET_APP_ID']

  def run(self):
    return self.request

  def request(self):
    response = urllib.request.urlopen(self.request_url())
    # Trimet API returns XML
    data = xmltodict.parse(response.read())
    return data

  def request_url(self):
    trimet_root =  "https://developer.trimet.org/ws/V1/arrivals"
    return trimet_root  + self.locations_string() + self.app_id_string()

  def app_id_string(self):
    return "&appID="+ self.tri_met_app_id

  def locations_string(self):
    return "?locIDs=" + ','.join(str(loc) for loc in self.locations)



