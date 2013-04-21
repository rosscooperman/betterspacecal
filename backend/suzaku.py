import time
import requests

from base_parser import BaseParser
from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup


class FermiParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'Suzaku'
    self._data_url = 'http://www.astro.isas.ac.jp/suzaku/schedule/shortterm/'
    self._datetime_format = '%Y %m %d %H %M %S'


  def fetch_schedule(self):
    try:
      html = requests.get(self._data_url).text
      soup = BeautifulSoup(html)
      schedule = list()
      lists = soup.findAll('li')[:2]
      for li in lists:
        page = self._data_url + li.find('a')['href']
        html = requests.get(page).text
        soup = BeautifulSoup(html)
        table = soup.find('table')
        rows = table.findAll('tr')[1:]
        for i in xrange(len(rows)):
          observation_1 = rows[i]
          if i < (len(rows) - 1):
            observation_2 = rows[i + 1]
          else:
            info_2 = None
            observation_2 = None
          info_1 = observation_1.findAll('td')
          if observation_2:
            info_2 = observation_2.findAll('td')
          try:
            coords = self._parse_coords(info_1[2].text, info_1[3].text)
          except:
            coords = None
          if coords:
            if info_2:
              end = datetime.strptime(info_2[6].text, self._datetime_format)
            else:
              end = datetime.strptime(info_1[6].text, self._datetime_format) + timedelta(hours=24)
            observation = {
                '_id'     : self._telescope + '|' + info_1[6].text,
                'source'  : self._telescope,
                'target'  : info_1[0].find('a').text,
                'ra'      : coords['ra_float'],
                'dec'     : coords['dec_float'],
                'ra_str'  : coords['ra_str'],
                'dec_str' : coords['dec_str'],
                'l'       : coords['l_float'],
                'b'       : coords['b_float'],
                'start'   : datetime.strptime(info_1[6].text, self._datetime_format),
                'end'     : end
             }
          schedule.append(observation)

      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None


if __name__ == '__main__':
  parser = FermiParser()
  parser.run()
