import time
import pymongo
import requests

from datetime import datetime
from BeautifulSoup import BeautifulSoup
from astropysics.coords import ICRSCoordinates, GalacticCoordinates


TELESCOPE = 'Fermi'
URL = 'http://fermi.gsfc.nasa.gov/ssc/observations/timeline/posting/'
# Formats at http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
DATETIME_FORMAT = '%Y-%j-%H:%M:%S'


def run():
  schedule = fetch_schedule()
  print schedule
  if schedule:
    save_schedule(schedule)


def save_schedule(schedule):
  try:
    conn = pymongo.MongoClient()
    db = conn['spacecalnyc']
    db.schedules.insert(schedule)
    print time.asctime() + ' | INFO | Sucessfully saved schedule for ' + TELESCOPE
  except Exception as e:
    print time.asctime() + ' | ERROR | Failed to save schedule for ' + TELESCOPE


def fetch_schedule():
  try:
    html = requests.get(URL).text
    soup = BeautifulSoup(html)
    schedule = list()
    table = soup.find('table', id="timelineTable")
    for row in table.findAll('tr'):
      info = row.findAll('td')
      if info:
        ra = info[6].text
        dec = info[7].text
        if ra:
          #print ra  + "," + dec
          coords = parseCoords(ra, dec)
          if coords:
            observation = {
              '_id'     : TELESCOPE + '|' + info[1].text,
              'source'  : TELESCOPE,
              'target'  : info[10].text,
              'ra'      : coords['ra_float'],
              'dec'     : coords['dec_float'],
              'ra_str'  : coords['ra_str'],
              'dec_str' : coords['dec_str'],
              'l'       : coords['l_float'],
              'b'       : coords['b_float'],
              'start'   : datetime.strptime(info[3].text, DATETIME_FORMAT),
              'end'     : datetime.strptime(info[4].text, DATETIME_FORMAT)
            }
            schedule.append(observation)
    return schedule
  except Exception as e:
    print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + TELESCOPE +'. Error: ' + str(e)
    return None


## this takes two strings in, one for the right ascension, and one for the declination
## this can be passed in with a range of formats. If it fails then it throws a
def parseCoords(ra_str,dec_str):
  try:
    float(ra_str)
    float(dec_str)
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
  except: 
    return None

if __name__ == '__main__':
  run()
