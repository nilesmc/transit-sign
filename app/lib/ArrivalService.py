import urllib, xmltodict
from flask import current_app as app

class ArrivalService():

  def __init__(self, locations):
    # must be list of locations
    self.locations = locations
    self.tri_met_app_id = app.config['TRI_MET_APP_ID']

  def get_arrivals(self):
    return self._groom_arrivals(self._request())

  # make the next two methods a parse class
  def _groom_arrivals(self, raw_arrivals):
    if not(self._arrivals_results_not_none(raw_arrivals)) :
      return raw_arrivals['resultSet']['arrival']

  def _arrivals_results_not_none(self, arrivals_data):
      return (arrivals_data.get('resultSet') is None or arrivals_data['resultSet'].get('arrival') is None)

  def _request(self):
    response = urllib.request.urlopen(self._request_url())
    # Trimet API returns XML
    return xmltodict.parse(response.read())

  def _request_url(self):
    return self._root_url()  + self._locations_string() + self._app_id_string()

  def _root_url(self):
    return "https://developer.trimet.org/ws/V1/arrivals"

  def _app_id_string(self):
    return "&appID="+ self.tri_met_app_id

  def _locations_string(self):
    return "?locIDs=" + ','.join(str(loc) for loc in self.locations)



