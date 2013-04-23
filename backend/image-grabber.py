import time
import urllib
import pymongo
import requests

from BeautifulSoup import BeautifulSoup

NED_DOMAIN = 'http://ned.ipac.caltech.edu'
NED_BASE_URL = NED_DOMAIN + '/cgi-bin/imgdata?objname='

SIMBAD_DOMAIN = 'http://simbad.u-strasbg.fr'
SIMBAD_BASE_URL = SIMBAD_DOMAIN + '/simbad/sim-id?Ident='
SIMBAD_IMAGE_URL_FORMAT = 'http://alasky.u-strasbg.fr/cgi/simbad-thumbnails/get-thumbnail.py?oid=%d&size=200&legend=false'


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
    all_targets = set(db.schedules.distinct('target'))
    target_scraped = set(db.target_images.distinct('_id'))
    return all_targets - target_scraped
  except Exception as e:
    print time.asctime() + ' | ERROR | Failed to get targets from database'
    return None


def get_images(target):
  images = get_images_from_NED(target)
  if not images:
    images = get_images_from_SIMBAD(target)

  if images:
    return {'_id': target, 'images': images}
  else:
    print 'No images found for ' + target
    return []


def get_images_from_NED(target):
  images = []
  try:
    url = NED_BASE_URL + urllib.quote(target)
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    rows = soup.findAll('tr')
    rows = rows[1:]
    for row in rows:
      image_url = NED_DOMAIN + row.find('td').find('a')['href']
      images.append(image_url)
    return images
  except Exception as e:
    print time.asctime() + ' | ERROR | Failed to get NED images for ' + target + '\n' + str(e)
    return []


def get_images_from_SIMBAD(target):
  """
      Sample image URL on SIMBAD:
      http://alasky.u-strasbg.fr/cgi/simbad-thumbnails/get-thumbnail.py?oid=3214151&
      size=200&legend=false&reticle=true&reticleWidth=1&reticleColor=yellow&scale=true
  """
  images = []
  try:
    url = SIMBAD_BASE_URL + urllib.quote(target)
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    image_tags = soup.findAll('img')
    for image in image_tags:
      if 'oid' in image['src']:  # if oid in img src, there is an image for this target
        image_url = image['src']
        images.append(image_url)
    return images
  except Exception as e:
    import traceback
    print time.asctime() + ' | ERROR | Failed to get SIMBAD images for ' + target + '\n' + traceback.format_exc()
    return []


if __name__ == '__main__':
  run()
