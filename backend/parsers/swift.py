import time
import requests

from base_parser import BaseParser
from datetime import datetime
from datetime import timedelta
from BeautifulSoup import BeautifulSoup


class FermiParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'Swift'
    self._data_url = 'https://www.swift.psu.edu/operations/obsSchedule.php?d=2013-04-21&a=0' # Changes per day


  def fetch_schedule(self):
    try:
      html = requests.get(self._data_url).text
      soup = BeautifulSoup(html)
      schedule = list()
      table = soup.find('table', attrs={'class': 'ppst'})
      for row in table.findAll('tr'):
        info = row.findAll('td')
        if info:
          try:
            ra = info[5].text.replace('&nbsp;','')
            dec = info[6].text.replace('&nbsp;','')
            if ra and dec:
              try:
                coords = self._parse_coords(ra, dec)
              except:
                coords = None
              if coords:
                observation = {
                  '_id'     : self._telescope + '|' + info[2].text.replace('&nbsp;','') + '|' + info[3].text.replace('&nbsp;',''),
                  'source'  : self._telescope,
                  'target'  : info[4].text.replace('&nbsp;',''),
                  'ra'      : coords['ra_float'],
                  'dec'     : coords['dec_float'],
                  'ra_str'  : coords['ra_str'],
                  'dec_str' : coords['dec_str'],
                  'l'       : coords['l_float'],
                  'b'       : coords['b_float'],
                  'start'   : datetime.strptime(info[0].text.replace('&nbsp;',''), self._datetime_format),
                  'end'     : datetime.strptime(info[1].text.replace('&nbsp;',''), self._datetime_format)
                }
                print observation
                schedule.append(observation)
          except:
            observation = None

      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None


if __name__ == '__main__':
  parser = FermiParser()
  parser.run()
