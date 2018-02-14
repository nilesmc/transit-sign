import click
from app import app
from app.lib import ArrivalService

@app.cli.group()
def arrival():
  """ Arrival Commands """
  # add in methods to reach out to Arrival service here
  pass

@arrival.command()
def update_all_arrival_times():
  """ Updates Arrival Times for every stop in the database"""

@arrival.command()
@click.argument('user_id')
def update_user_arrival_times(user_id):
  """ Updates Arrival Times for one user"""
  user = User(user_id)
  stops = User.stops.filter(lambda stop: stop in stops, stop_id)
  arrival_times =  ArrivalService.ArrivalService(stops)
  return arrival_times

@arrival.command()
@click.argument('stop_id')
def update_stop_arrival_times(stop_id):
  """ Updates Arrival Times for a stop or stops"""
  arrival_times = ArrivalService.ArrivalService([stop_id])
  return arrival_times

