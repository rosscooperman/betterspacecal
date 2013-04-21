import traceback
import time
import requests

from base_parser import BaseParser
from datetime import datetime
from BeautifulSoup import BeautifulSoup


class FermiParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'INTEGRAL'
    self._data_url = 'http://integral.esac.esa.int/isocweb/schedule.html?action=intro'
    self._datetime_format = '%Y-%m-%d %H:%M:%S'


  def fetch_schedule(self):
    try:
      html = requests.get(self._data_url).text
      soup = BeautifulSoup(html)
      schedule = list()
      tables = soup.findAll('table')
      schedule_table = tables[2]
      rows = schedule_table.findAll('tr')
      rows = rows[:-1]  # Skip the last row, which has the map
      for row in rows:
        info = row.findAll('td')
        if info:
          ra = info[5].text
          dec = info[6].text
          if ra and dec:
            try:
              coords = self._parse_coords(ra, dec)
            except:
              coords = None
            if coords:
              observation = {
                '_id'     : self._telescope + '|' + info[10].text,
                'source'  : self._telescope,
                'target'  : info[4].text,
                'ra'      : coords['ra_float'],
                'dec'     : coords['dec_float'],
                'ra_str'  : coords['ra_str'],
                'dec_str' : coords['dec_str'],
                'l'       : coords['l_float'],
                'b'       : coords['b_float'],
                'start'   : datetime.strptime(info[1].text, self._datetime_format),
                'end'     : datetime.strptime(info[2].text, self._datetime_format)
              }
              schedule.append(observation)
      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + traceback.format_exc()
      return None


if __name__ == '__main__':
  parser = FermiParser()
  parser.run()

