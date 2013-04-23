import time
import requests

from base_parser import BaseParser
from datetime import datetime


class HubbleParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'Hubble'


  def fetch_schedule(self):
    try:
      schedule = list()
      for line in open( "hubble.txt", "r" ):
        info = line.split("\t")
        ra = info[2]
        dec = info[3]
        print ra  + dec
        if ra and dec:
          try:
            coords = self._parse_coords(ra, dec)
          except:
            coords = None
          if coords:
            observation = {
                  '_id'     : self._telescope + '|' + info[0],
                  'source'  : self._telescope,
                  'target'  : info[1],
                  'ra'      : coords['ra_float'],
                  'dec'     : coords['dec_float'],
                  'ra_str'  : coords['ra_str'],
                  'dec_str' : coords['dec_str'],
                  'l'       : coords['l_float'],
                  'b'       : coords['b_float'],
                  'start'   : datetime.strptime(info[5], self._datetime_format),
                  'end'     : datetime.strptime(info[6], self._datetime_format)
            }
            print observation
            schedule.append(observation)
      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None


if __name__ == '__main__':
  parser = HubbleParser()
  parser.run()
