import time
import urllib
import urlparse
import pymongo
import requests

from BeautifulSoup import BeautifulSoup

NED_DOMAIN = 'http://ned.ipac.caltech.edu'
NED_BASE_URL = NED_DOMAIN + '/cgi-bin/imgdata?objname='

SIMBAD_DOMAIN = 'http://simbad.u-strasbg.fr'
SIMBAD_BASE_URL = SIMBAD_DOMAIN + '/simbad/sim-id?Ident='
SIMBAD_IMAGE_URL_FORMAT = 'http://alasky.u-strasbg.fr/cgi/simbad-thumbnails/get-thumbnail.py?oid=%s&size=200&legend=false'
BULK_INSERTION_SIZE = 25  # Dump to Mongo after we parse N targets

def run():
  targets = get_targets()
  images_list = list()
  for t in targets:
    target_images = get_images(t)
    if target_images:
      images_list.append(target_images)
      if len(images_list) == BULK_INSERTION_SIZE:
        save_images(images_list)
        images_list = list()

  # Dump remaining images to Mongo if any
  if images_list:
    save_images(images_list)


def save_images(images):
  try:
    conn = pymongo.MongoClient()
    db = conn['spacecalnyc']
    for target in images:
      # Update schedules with target images
      db.schedules.update({'target': target['_id']},
          {'$set': {'images': target['images'],
                    'reference_url': target['reference_url']}},
          multi=True)
    print time.asctime() + ' | INFO | Successfully saved images for ' + str(len(images)) + ' targets.'
  except Exception as e:
    print time.asctime() + ' | ERROR | Failed to save images to database' + str(e)


def get_targets():
  try:
    conn = pymongo.MongoClient()
    db = conn['spacecalnyc']
    all_targets = set(db.schedules.distinct('target'))
    scraped_targets = set(db.command(
        {'distinct': 'schedules',
          'query'  : {'images': {'$ne': None}},
          'key'    : 'target'})
        ['values'])
    return all_targets - scraped_targets
  except Exception as e:
    print time.asctime() + ' | ERROR | Failed to get targets from database'
    return None


def get_images(target):
  images = get_images_from_NED(target)
  reference_url = NED_BASE_URL + urllib.quote(target)
  if not images:
    images = get_images_from_SIMBAD(target)
    reference_url = SIMBAD_BASE_URL + urllib.quote(target)

  if images:
    return {'_id': target, 'images': images, 'reference_url': reference_url}
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
        image_url = get_simbad_image_url(image['src'])
        images.append(image_url)
    return images
  except Exception as e:
    import traceback
    print time.asctime() + ' | ERROR | Failed to get SIMBAD images for ' + target + '\n' + traceback.format_exc()
    return []


# This method removes the recticle, scale etc. parameters from the image URL.
def get_simbad_image_url(url):
  parse_result = urlparse.urlparse(url)
  query = urlparse.parse_qs(parse_result.query)
  oid = query['oid'][0]
  return SIMBAD_IMAGE_URL_FORMAT % oid


if __name__ == '__main__':
  run()
