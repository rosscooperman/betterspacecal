import time
import requests

from base_parser import BaseParser
from datetime import datetime
from BeautifulSoup import BeautifulSoup


class NuStarParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'NuStar'
    self._data_url = 'http://www.srl.caltech.edu/NuSTAR_Public/NuSTAROperationSite/AFT_Public.php'
    self._datetime_format = '%Y:%j:%H:%M:%S'


  def fetch_schedule(self):
    try:
      html = requests.get(self._data_url).text
      soup = BeautifulSoup(html)
      schedule = list()
      table = soup.find('table', id='priority-table')
      for row in table.findAll('tr'):
        info = row.findAll('td')
        if info:
          ra = info[4].text
          dec = info[5].text
          if ra and dec:
            try:
              coords = self._parse_coords(ra, dec)
            except:
              coords = None
            if coords:
              observation = {
                '_id'     : self._telescope + '|' + info[2].text,
                'source'  : self._telescope,
                'target'  : info[3].text,
                'ra'      : coords['ra_float'],
                'dec'     : coords['dec_float'],
                'ra_str'  : coords['ra_str'],
                'dec_str' : coords['dec_str'],
                'l'       : coords['l_float'],
                'b'       : coords['b_float'],
                'start'   : datetime.strptime(info[0].text, self._datetime_format),
                'end'     : datetime.strptime(info[1].text, self._datetime_format)
              }
              schedule.append(observation)

      return schedule
    except Exception as e:
      import traceback
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + traceback.format_exc()
      return None


if __name__ == '__main__':
  parser = NuStarParser()
  parser.run()

