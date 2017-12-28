# NextBus API service.
# Required Inputs: Information Transit agency, bus line, direction and stop
# Returns a hash with arrival data

import urllib
from xml.dom.minidom import parseString

class TriMetService:

  def __init__(self, locations):
    self.locations = locations

  def run():
    parseString(req)

  def req():
    embed()
    connection = urllib.urlopen(
      'https://developer.trimet.org/ws/V1/arrivals/loc_ids' +
      loc_ids +
      app_id
    )
    raw = connection.read()
    connection.close()
    return raw

  def app_id():
    'appID' + config.TRI_MET_APP_ID

  def config():
    yaml.safe_load(open("./config.yml"))

  def loc_ids(locations):
    ''.join(locations)
