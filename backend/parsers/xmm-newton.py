import time
import requests

from base_parser import BaseParser
from datetime import datetime
from BeautifulSoup import BeautifulSoup


class XMMNewtonParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'XMM-Newton'
    self._data_url = 'http://xmm2.esac.esa.int/external/xmm_sched/short_term_schedule.php'


  def fetch_schedule(self):
    try:
      html = requests.get(self._data_url).text
      soup = BeautifulSoup(html)
      schedule = list()
      for row in soup.findAll('tr', attrs={'align': 'CENTER'}):
        info = row.findAll('td')
        coords = self._parse_coords(info[3].text, info[4].text)
        observation = {
              '_id'     : self._telescope + '|' + info[1].find('a').text,
              'source'  : self._telescope,
              'target'  : info[2].text,
              'ra'      : coords['ra_float'],
              'dec'     : coords['dec_float'],
              'ra_str'  : coords['ra_str'],
              'dec_str' : coords['dec_str'],
              'l'       : coords['l_float'],
              'b'       : coords['b_float'],
              'start'   : datetime.strptime(info[6].text, self._datetime_format),
              'end'     : datetime.strptime(info[7].text, self._datetime_format)
        }
        schedule.append(observation)
      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None


if __name__ == '__main__':
  parser = XMMNewtonParser()
  parser.run()
