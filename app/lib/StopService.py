import urllib, xmltodict
from flask import current_app as app

class StopService():

  def __init__(self, location):
    # must be list of lat-long pair
    self.location = location
    self.tri_met_app_id = app.config['TRI_MET_APP_ID']

  def get_stops(self):
    raw_stops = self.request()

    if raw_stops.get('resultSet') is None or raw_stops['resultSet'].get('location') is None : return
    else:
      raw_stops = self.request()['resultSet']['location']

    stops = []
    for stop in raw_stops:
      stops.append({
        'id': stop['@locid'],
        'address': stop['@desc'],
        'latitude': stop['@lat'],
        'longitude': stop['@lng'],
        'direction': stop['@dir']
       })

    return stops

  def request(self):
    response = urllib.request.urlopen(self.request_url())
    # Trimet API returns XML
    data = xmltodict.parse(response.read())
    return data

  def request_url(self):
    trimet_root =  "https://developer.trimet.org/ws/V1/stops"
    return trimet_root  + self.location_string() + self.meters_string() + self.app_id_string()

  def app_id_string(self):
    return "&appID="+ self.tri_met_app_id

  def location_string(self):
    return "/ll/" + ','.join(str(loc) for loc in self.location)

  def meters_string(self):
    return "/meters/200"
