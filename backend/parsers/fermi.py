import time
import requests

from base_parser import BaseParser
from datetime import datetime
from BeautifulSoup import BeautifulSoup


class FermiParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'Fermi'
    self._data_url = 'http://fermi.gsfc.nasa.gov/ssc/observations/timeline/posting/'
    self._datetime_format = '%Y-%j-%H:%M:%S'


  def fetch_schedule(self):
    try:
      html = requests.get(self._data_url).text
      soup = BeautifulSoup(html)
      schedule = list()
      table = soup.find('table', id='timelineTable')
      for row in table.findAll('tr'):
        info = row.findAll('td')
        if info:
          ra = info[6].text
          dec = info[7].text
          if ra and dec:
            try:
              coords = self._parse_coords(ra, dec)
            except:
              coords = None
            if coords:
              observation = {
                '_id'     : self._telescope + '|' + info[1].text,
                'source'  : self._telescope,
                'target'  : info[10].text,
                'ra'      : coords['ra_float'],
                'dec'     : coords['dec_float'],
                'ra_str'  : coords['ra_str'],
                'dec_str' : coords['dec_str'],
                'l'       : coords['l_float'],
                'b'       : coords['b_float'],
                'start'   : datetime.strptime(info[3].text, self._datetime_format),
                'end'     : datetime.strptime(info[4].text, self._datetime_format)
              }
              schedule.append(observation)

      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None


if __name__ == '__main__':
  parser = FermiParser()
  parser.run()
