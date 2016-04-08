import ConfigParser
from ftplib import FTP
import requests

# Get values from configuration file
config = ConfigParser.RawConfigParser()
config.read('GroupMeConfig.cfg')

# GroupMe Variables
token = config.get('GroupMe', 'token') 
groupme_api_url = config.get('GroupMe', 'groupme_api_url')
groupme_image_url = config.get('GroupMe', 'groupme_image_url')
bot_id = config.get('GroupMe', 'bot_id')

# FTP Variables
host = config.get('FTP', 'host')
user = config.get('FTP', 'user')
passwd = config.get('FTP', 'passwd')

# Instantiate message components
text = ''
data = {}
attachments = []

# Populate fields
data['text'] = raw_input('Enter text to place in message: ')
data['bot_id'] = bot_id

def group_listing():
    # Get list of groups user is a member of
    r = requests.get('%s/groups?token=%s' % (groupme_api_url, token))
    resp = r.json()

    print 'Groups:'
    for item in resp['response']:
        print item['name']

# Get image(s) from FTP server
ftp = FTP(host)
ftp.login(user, passwd) 

imageSet = set()

# Add every .jpg image in current FTP directory to set
for filename in ftp.nlst():
    if '.jpg' in filename:
        imageSet.add(filename)

# Download every .jpg image found in previous step to current directory
for image in imageSet:
    print 'Downloading %s...' % image
    ftp.retrbinary('RETR %s' % image, open(image, 'wb').write)
ftp.quit()

# While still images left to upload...
while len(imageSet):
    filename = imageSet.pop()
    files = {'file': open(filename, 'rb')}
    print 'Uploading %s to GroupMe image service...' % filename
    # Upload image to GroupMe image service
    r = requests.post('%s?access_token=%s' % (groupme_image_url, token), files=files)
    # Get URL of image as given by GroupMe image service
    image_url = r.json()['payload']['url']
    # Attach image
    attachments.append({'type': 'image', 'url': image_url})
    # Attach location
    attachments.append({'type': 'location', 'lng': '-73.993285', 'lat': '40.738206', 'name': 'GroupMe HQ'})

    # Populate final data field to be POSTed
    data['attachments'] = attachments

    # Post text, image, and location to group chat
    print 'POSTing message to GroupMe...'
    r = requests.post('%s/bots/post' % groupme_api_url, json = data)
    # Clear attachments to avoid re-posting same content
    del attachments[:]
