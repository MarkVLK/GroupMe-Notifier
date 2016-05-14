# GroupMe-Notifier

This is a simple Python script that will have a GroupMe Bot post a message containing text, an image, and/or a location to whatever group it is attached to.

At the moment, it works as such:

1.  Reads from GroupMeConfig.cfg file to populate necessary variables
2.  Connects to an FTP server using the user & host specified in the config file
3.  Downloads the first and last .jpg file from the image directory of the FTP server specified in the config file to the local current directory (directory that GroupMeNotify.py was run from)
4.  Uploads every .jpg file downloaded to the GroupMe image service
5.  For every image downloaded, sends a message to the Bot's group containing the image and the name of the image then deletes the image from the local device

Please note that there is currently very little error checking which means that if you don't provide a valid value for every item in the config file you will receive an exception and the script will prematurely stop.
