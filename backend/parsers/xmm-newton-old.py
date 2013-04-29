import time
import requests
import sys

from base_parser import BaseParser
from datetime import datetime
from BeautifulSoup import BeautifulSoup


class XMMNewtonParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'XMM-Newton'
    #self._data_url = 'http://xmm2.esac.esa.int/external/xmm_sched/short_term_schedule.php'
    self._datetime_format = '%Y-%m-%d | %H:%M:%S'



  def fetch_schedule(self):
    try:
      filename=sys.argv[1]
      f = open(filename,"r")
      html = f.read()
      soup = BeautifulSoup(html)
      schedule = list()
      table = soup.find('table', attrs={'align': 'LEFT'})
      nextline=False
      for row in table.findAll('tr'):
        info = row.findAll('td')
        type=info[2].text
        if nextline:
          obid = info[2].text.replace("ID:","").strip()
          target = info[3].text
          nextline = False
          print obid +  "," + target
        if type == 'OBS_START':
          start=info[1].text
          ra=info[3].text.replace("RA:","").strip()
          dec=info[4].text.replace("DEC:","").strip()
          print ra + "," +  dec
          nextline = True
        if type == 'OBS_END':
          end=info[1].text
          print start + "," + end
          coords = self._parse_coords(ra, dec)
          observation = {
              '_id'     : self._telescope + '|' + obid,
              'source'  : self._telescope,
              'target'  : target,
              'ra'      : coords['ra_float'],
              'dec'     : coords['dec_float'],
              'ra_str'  : coords['ra_str'],
              'dec_str' : coords['dec_str'],
              'l'       : coords['l_float'],
              'b'       : coords['b_float'],
              'start'   : datetime.strptime(start, self._datetime_format),
              'end'     : datetime.strptime(end, self._datetime_format)
          }
          schedule.append(observation)
      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None


if __name__ == '__main__':
  parser = XMMNewtonParser()
  parser.run()
