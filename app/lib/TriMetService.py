import urllib, xmltodict

class TriMetService():

  def __init__(self, locations):
    self.locations = locations
    self.tri_me_app_id = app.config.tri_me_app_id

  def run(self):
    return request

  def request(self):
    response = urlib.request.get(self.request_url)
    data = xmltodict(response)

  def request_url(self):
    trimet_root =  "https://developer.trimet.org/ws/V1/arrivals?"
    return trimet_root  + locations_string + app_id_string

  def app_id_string(self):
    return "&appID="+ self.tri_me_app_id

  def locations_string(self):
    return "?locations=" + ",".joins(str(location) for location in locations)



