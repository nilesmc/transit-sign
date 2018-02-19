import urllib, xmltodict
from flask import current_app as app

class StopService():

  def __init__(self, location, distance='200'):
    # must be list of lat-long pair
    self.location = location
    self.distance = distance
    self.tri_met_app_id = app.config['TRI_MET_APP_ID']

  def get_stops(self):
    raw_stops = self._request()

    if raw_stops.get('resultSet') is None or raw_stops['resultSet'].get('location') is None : return
    else:
      raw_stops = raw_stops['resultSet']['location']

    # move this onto the stop model
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

  def _request(self):
    response = urllib.request.urlopen(self._request_url())
    # Trimet API returns XML
    return xmltodict.parse(response.read())

  def _request_url(self):
    return self._root_url()  + self._location_string() + self._meters_string() + self._app_id_string()

  def _root_url(self):
    return "https://developer.trimet.org/ws/V1/stops"

  def _app_id_string(self):
    return "&appID="+ self.tri_met_app_id

  def _location_string(self):
    return "/ll/" + ','.join(str(loc) for loc in self.location)

  def _meters_string(self):
    return "/meters/" + self.distance
