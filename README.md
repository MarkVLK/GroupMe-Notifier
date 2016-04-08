# GroupMe-Notifier

This is a simple Python script that will have a GroupMe Bot post a message containing text, an image, and a location to whatever group it is attached to.

At the moment, it works as such:

1.  Reads from GroupMeConfig.cfg file to populate necessary variables
2.  Asks user to input text they'd like to send in the GroupMe message
3.  Connects to an FTP server using the user & host specified in the config file
4.  Downloads every .jpg file in the root directory of the FTP user/server specified to the current directory (directory that GroupMeNotify.py was run from)
5.  Uploads every .jpg file downloaded to the GroupMe image service
6.  For every image downloaded, sends a message to the Bot's group containing the text entered in step 2, the image, and the GroupMe HQ location (hard coded for now)

This means that for however many .jpg images found & downloaded, that many messages will be sent to the Bot's group with the same text and same location (GroupMe HQ). This will be changed eventually, this project is still in its testing stage...

Please note that there currently is no error checking which means that if you don't provide everything the Python script excepts (all config variables, .jpg images in FTP user/server root directory, etc.) you will probably just receive an exception and the script will prematurely stop.
