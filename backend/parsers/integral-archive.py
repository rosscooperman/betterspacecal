import sys
import time
import requests

from base_parser import BaseParser
from datetime import datetime


class INTEGRALArchiveParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'INTEGRAL'
    self._datetime_format = '%Y-%m-%d %H:%M:%S.0'


  def fetch_schedule(self):
    try:
      schedule = list()
      filename=sys.argv[1]
      for line in open(filename, "r" ):
        info = line.split(",")
        #"10","2002-11-15 01:25:00.0","2002-11-15 01:41:40.0","1000","empty field 1","09:59:21.79","-00:58:55.2","Staring"," Public","0060001","0060001 / 0001",
        for i in range(0,len(info)):
          #print info[i]
          info[i] = info[i].replace('"','')
        start = info[1]
        end = info[2]
        ra = info[5]
        dec = info[6]
        obsid=info[10]
        if ra and dec:
          print ra + "," + dec
          try:
            coords = self._parse_coords(ra, dec)
          except:
            coords = None
          if coords:
            print start + "," + end
            observation = {
                  '_id'     : self._telescope + '|' + obsid,
                  'observation': obsid,
                  'source'  : self._telescope,
                  'target'  : info[4],
                  'ra'      : coords['ra_float'],
                  'dec'     : coords['dec_float'],
                  'ra_str'  : coords['ra_str'],
                  'dec_str' : coords['dec_str'],
                  'l'       : coords['l_float'],
                  'b'       : coords['b_float'],
                  'start'   : datetime.strptime(start, self._datetime_format),
                  'end'     : datetime.strptime(end, self._datetime_format)
            }
            print observation
            schedule.append(observation)
      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None


if __name__ == '__main__':
  parser = INTEGRALArchiveParser()
  parser.run()
