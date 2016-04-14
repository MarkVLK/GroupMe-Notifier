import ConfigParser
#from datetime import datetime
from ftplib import FTP_TLS
import os
import requests

# Get values from configuration file
config = ConfigParser.RawConfigParser()
config.read('GroupMeConfig.cfg')

# GroupMe Variables
TOKEN = config.get('GroupMe', 'token')
GROUPME_API_URL = config.get('GroupMe', 'groupme_api_url')
GROUPME_IMAGE_URL = config.get('GroupMe', 'groupme_image_url')
BOT_ID = config.get('GroupMe', 'bot_id')

# FTP Variables
HOST = config.get('FTP', 'host')
USER = config.get('FTP', 'user')
PASSWD = config.get('FTP', 'passwd')
IMAGE_DIRECTORY = config.get('FTP', 'image_directory')

# Instantiate message components
data = {}
attachments = []

# Populate fields
#data['text'] = raw_input('Enter text to place in message: ')
data['bot_id'] = BOT_ID

def group_listing():
    # Get list of groups user is a member of
    r = requests.get('%s/groups?token=%s' % (GROUPME_API_URL, TOKEN))
    resp = r.json()

    print 'Groups:'
    for item in resp['response']:
        print item['name']

# Securely connect to FTP server
ftps = FTP_TLS(HOST, USER, PASSWD)
ftps.prot_p()
# Change working directory to directory containing images
ftps.cwd(IMAGE_DIRECTORY)
# Get list of items in current directory
directory_list = ftps.nlst()
# Get list of images
image_list = [item for item in directory_list if '.jpg' in item]
# Save oldest & newest images
images_to_upload = []
if image_list:
    # Add first image
    images_to_upload.append(image_list[0])
    if len(image_list) > 1:
        # Add last image (if more than 1 image)
        images_to_upload.append(image_list[len(image_list)-1])
    # Download oldest & newest image
    for image in images_to_upload:
        print 'Downloading %s...' % image
        ftps.retrbinary('RETR %s' % image, open(image, 'wb').write)

# Check if directory for old images exists, if not create it
if 'old' not in directory_list:
    print 'Creating dir "old"...'
    ftps.mkd('old')

# Move checked images to old
for image in image_list:
    #date_str = image.split('_')[1].split('.')[0]
    #img_date = datetime.strptime(date_str, '%Y%m%d-%H%M%S')
    print 'Moving %s to "old"...' % image
    ftps.rename(image, 'old/%s' % image)

# Disconnect from FTP server
ftps.quit()

def upload_image(filename):
    image_file = {'file': open(filename, 'rb')}
    print 'Uploading %s to GroupMe image service...' % filename
    r = requests.post('%s?access_token=%s' % (GROUPME_IMAGE_URL, TOKEN), files=image_file)
    # Get URL of image as given by GroupMe image service
    return r.json()['payload']['url']

# Upload images to GroupMe image service
for image in images_to_upload:
    image_url = upload_image(image)
    # Delete image from local storage
    print 'Deleting %s...' % image
    os.remove(image)
    # Attach image to message
    attachments.append({'type': 'image', 'url': image_url})
    # Attach location to message
    #attachments.append({'type': 'location', 'lng': '-73.993285', 'lat': '40.738206', 'name': 'GroupMe HQ'})

    # Populate final data field to be POSTed
    data['attachments'] = attachments
    data['text'] = image

    # Post text, image, and location to group chat
    print 'POSTing message to GroupMe...'
    r = requests.post('%s/bots/post' % GROUPME_API_URL, json=data)
    # Clear attachments to avoid re-posting same content
    del attachments[:]
