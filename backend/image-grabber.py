import time
import urllib
import pymongo
import requests

from PIL import Image
from BeautifulSoup import BeautifulSoup

DOMAIN = 'http://ned.ipac.caltech.edu/'
BASE_URL = DOMAIN + 'cgi-bin/imgdata?objname='

def run():
  targets = get_targets()
  images_list = list()
  for t in targets:
    target_images = get_images(t)
    if target_images:
      images_list.append(target_images)
  if images_list:
    save_images(images_list)


def save_images(images):
  try:
    conn = pymongo.MongoClient()
    db = conn['spacecalnyc']
    for target in images:
      db.target_images.save(target)
    print time.asctime() + ' | INFO | Successfully saved images'
  except Exception as e:
    print time.asctime() + ' | ERROR | Failed to save images to database' + str(e)


def get_targets():
  try:
    conn = pymongo.MongoClient()
    db = conn['spacecalnyc']
    targets = db.schedules.distinct('target')
    return targets
  except Exception as e:
    print time.asctime() + ' | ERROR | Failed to get targets from database'
    return None


def get_images(target):
  images = []
  try:
    url = BASE_URL + urllib.quote(target)
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    rows = soup.findAll('tr')
    rows = rows[1:]
    for row in rows:
      image_url = DOMAIN + row.find('td').find('a')['href']
      images.append(image_url)
    if images:
      return {'_id': target, 'images': images}
    else:
      print 'No images for ' + target
      return None
  except Exception as e:
    print time.asctime() + ' | ERROR | Failed to get images for ' + target + '\n' + str(e)
    return None


if __name__ == '__main__':
  run()
