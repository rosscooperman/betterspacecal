import time
import pymongo
import requests

from datetime import datetime
from BeautifulSoup import BeautifulSoup
from astropysics.coords import ICRSCoordinates, GalacticCoordinates

class BaseParser:
  def __init__(self):
    self._conn = None
    self._telescope = 'BaseTelescope'
    self._data_url = None
    self._datetime_format = '%Y-%m-%d %H:%M:%S'
    self._init_db()


  def _init_db(self):
    try:
      self._conn = pymongo.MongoClient()
      self._db = self._conn['spacecalnyc']
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to init database, exiting...'
      self._exit()


  def run(self):
    schedule = self.fetch_schedule()
    if schedule:
      self.save_schedule(schedule)
    self._exit()


  def fetch_schedule(self):
    print time.asctime() + ' | ERROR | fetch_schedule not implemented for ' + \
        self._telescope
    return None


  def save_schedule(self, schedule):
    try:
      for observation in schedule:
        self._db.schedules.save(observation)
      print time.asctime() + ' | INFO | Sucessfully saved schedule for ' + \
          self._telescope
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to save schedule for ' + \
          self._telescope + ' ' + str(e)


  ## this takes two strings in, one for the right ascension, and one for the declination
  ## this can be passed in with a range of formats. If it fails then it throws a
  def _parse_coords(self, ra_str, dec_str):
    eq_coords = ICRSCoordinates(ra_str,dec_str)
    gal_coords = eq_coords.convert(GalacticCoordinates)
    return {
        'ra_float'  : eq_coords.ra.degrees,
        'dec_float' : eq_coords.dec.degrees,
        'l_float'   : gal_coords.l.degrees,
        'b_float'   : gal_coords.b.degrees,
        'ra_str'    : eq_coords.ra.getHmsStr(),
        'dec_str'   : eq_coords.dec.getDmsStr(sep=('d', 'm', 's'))
     }

  def _exit(self):
    if self._conn:
      self._conn.close()
