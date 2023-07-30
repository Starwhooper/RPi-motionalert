#!/usr/bin/python3
# Creator: Thiemo Schuff, thiemo@schuff.eu
# Source: https://github.com/Starwhooper/RPi-motionalert

#######################################################
#
# Prepare
#
#######################################################

# -*- coding:utf-8 -*-
#from PIL import Image,ImageDraw,ImageFont,ImageColor
#from datetime import datetime
#import RPi.GPIO as GPIO
import argparse
import json
import os
import requests
#import subprocess
import sys
import time
#import urllib.request

scriptfolder = os.path.split(os.path.abspath(__file__))[0]

##### import config.json
try:
 with open(scriptfolder + '/config.json','r') as file:
  cf = json.loads(file.read())
except:
 sys.exit('exit: The configuration file ' + scriptfolder + '/config.json does not exist or has incorrect content. Please rename the file config.json.example to config.json and change the content as required ')

if (os.path.isdir(cf['folder'])) == False : sys.exit('exit: folder ' + cf['folder'] + ' not found, please check parameter folder in file ' + scriptfolder + '/config.json. This folder typical includes the Folder Camera1, Camera2, Camera3 ...')

parser = argparse.ArgumentParser(
    prog='RPI-motionalery by Starwhooper',
    description="send pushover messager for motion",
    epilog='keep watching https://github.com/Starwhooper/RPi-motionalert')

parser.add_argument(
    "-c", "--cameraid", 
    type=int, 
    choices=range(1,11), 
    help="ID of camera")

parser.add_argument(
    "-p", "--picture", 
    type=str,
    default='',
    help="Path to picture file")

parser.add_argument(
    "-m", "--messagebody", 
    type=str, 
    default='any movement detected', 
    help="Text that should be displayed in pushover message")
    
parser.add_argument(
    "-t", "--messagetitle", 
    type=str, 
    default='', 
    help="if not set, send ID of camera")

parser.add_argument(
    "-v", "--verbose", 
    action='store_true', 
    help="verbose feedback")

args = parser.parse_args()

if (os.path.isdir(cf['folder'] + "/Camera" + str(args.cameraid))) == False : sys.exit('exit: folder ' + cf['folder'] + '/Camera' + str(args.cameraid) + ' not found, please check camera ID')

if (len(args.picture) >= 1):
    if (os.path.isfile(cf['folder'] + "/Camera" + str(args.cameraid) + '/' + args.picture)) == False : sys.exit('exit: ' + cf['folder'] + "/Camera" + str(args.cameraid) + '/' + args.picture + ' not found')
    time.sleep(2)
    output_picturepath = cf['folder'] + "/Camera" + str(args.cameraid) + '/' + args.picture
else: output_picturepath = scriptfolder + "/example.gif"

if (args.messagetitle == ''): output_messagetitle = "Camera " + str(args.cameraid)
else: output_messagetitle = args.messagetitle

output_messagebody = args.messagebody

##### send message
r = requests.post("https://api.pushover.net/1/messages.json", data = {
  "token": cf['pushover']['apikey'],
  "user": cf['pushover']['userkey'],
  "message": output_messagebody,
  "title": output_messagetitle # - your message's title, otherwise your app's name is used

# ,   attachment_base64 - a Base64-encoded image attachment to send with the message (documentation)
# ,   attachment_type - the MIME type of the included attachment or attachment_base64 (documentation)
# ,   device - the name of one of your devices to send just to that device instead of all devices (documentation)
# ,   html - set to 1 to enable HTML parsing (documentation)
# ,   priority - a value of -2, -1, 0 (default), 1, or 2 (documentation)
# ,   sound - the name of a supported sound to override your default sound choice (documentation)
# ,   timestamp - a Unix timestamp of a time to display instead of when our API received it (documentation)
# ,   ttl - a number of seconds that the message will live, before being deleted automatically (documentation)
# ,   url - a supplementary URL to show with your message (documentation)
# ,   url_title - a title for the URL specified as the url parameter, otherwise just the URL is shown (documentation) 
  
},
files = {
  "attachment": ("image.jpg", open(output_picturepath, "rb"), "image/gif")
})

if args.verbose == True: 
    print(r.text)
    print (output_picturepath)

