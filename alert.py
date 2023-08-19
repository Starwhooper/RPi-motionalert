#!/usr/bin/python
# Creator: Thiemo Schuff, thiemo@schuff.eu
# Source: https://github.com/Starwhooper/RPi-motionalert

#######################################################
#
# Prepare
#
#######################################################

# -*- coding:utf-8 -*-
from ffmpeg import FFmpeg, Progress
import argparse
import glob
import json
import os
import pathlib
import requests
import sys
import time


scriptfolder = os.path.split(os.path.abspath(__file__))[0]

##### import config.json
try:
 with open(scriptfolder + '/config.json','r') as file:
  cf = json.loads(file.read())
except:
 sys.exit('exit: The configuration file ' + scriptfolder + '/config.json does not exist or has incorrect content. Please rename the file config.json.example to config.json and change the content as required ')

if (os.path.isdir(cf['camerafolder'])) == False : sys.exit('exit: folder ' + cf['camerafolder'] + ' not found, please check parameter folder in file ' + scriptfolder + '/config.json. This folder typical includes the Folder Camera1, Camera2, Camera3 ...')

parser = argparse.ArgumentParser(
    prog='RPI-motionalery by Starwhooper',
    description="send pushover messager for motion",
    epilog='keep watching https://github.com/Starwhooper/RPi-motionalert')

parser.add_argument(
    "-a", "--animation", 
    action='store_true', 
    help="convert video to gif animation (makes only sense as event after motion has ended")

parser.add_argument(
    "-ka", "--keepanimation", 
    action='store_true', 
    help="let the animation keep alive, mean that GIF will not be deleted after sending")

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
output_messagebody = ""

if (os.path.isdir(cf['camerafolder'] + "/Camera" + str(args.cameraid))) == False : sys.exit('exit: folder ' + cf['camerafolder'] + '/Camera' + str(args.cameraid) + ' not found, please check camera ID')

if (len(args.picture) >= 1):
    if (args.animation == False):
        if (os.path.isfile(cf['camerafolder'] + "/Camera" + str(args.cameraid) + '/' + args.picture)) == False : sys.exit('exit: ' + cf['camerafolder'] + "/Camera" + str(args.cameraid) + '/' + args.picture + ' not found')
        time.sleep(2)
        output_picturepath = cf['camerafolder'] + "/Camera" + str(args.cameraid) + '/' + args.picture
    else:
        newestdate = newestfile = 0
        for file in glob.glob(cf['camerafolder'] + "/Camera" + str(args.cameraid) + '/' + args.picture, recursive=False):
            if newestdate <= os.path.getmtime(file):
                newestdate = os.path.getmtime(file)
                newestfile = file
        if (newestfile != 0):
            ffmpeg = (
                FFmpeg()
                .option("y")
                .input(newestfile)
                .output(
                    newestfile+".gif",
                    vf="scale=320:-1"
                )
            )

            #best quality:
            #ffmpeg -i 20-22-20.avi -filter_complex "[0:v] palettegen" 20-22-20.palette.png
            #ffmpeg -i 20-22-20.avi -i 20-22-20.palette.png -filter_complex "[0:v] fps=25,scale=320:-1 [new];[new][1:v] paletteuse" 20-22-20.best.gif
            #oneliner: ffmpeg -y -i 20-22-20.avi -filter_complex "scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse=dither=bayer" small.gif
            try:
                ffmpeg.execute()
                output_picturepath = newestfile+".gif"
            except:
                print("FAILED: ffmpeg -y -i " + newestfile + " -filter_complex \"scale=320:-1\" " + newestfile + ".gif")
                output_messagebody = output_messagebody + "could not convert video to gif\n"
                output_picturepath = scriptfolder + "/" + cf['exampleanimation']
        else:
            output_picturepath = scriptfolder + "/" + cf['exampleanimation']
            output_messagebody = output_messagebody + "No media found: " + cf['camerafolder'] + "/Camera" + str(args.cameraid) + '/' + args.picture + "\n"
else: 
    output_picturepath = scriptfolder + "/" + cf['exampleanimation']

stats = os.stat(output_picturepath)

if  (stats.st_size > cf['pushover']['maxattachmentsize']): output_picturepath = scriptfolder + "/example.gif"

if (args.messagetitle == ''): output_messagetitle = "Camera " + str(args.cameraid)
else: output_messagetitle = args.messagetitle

if (args.animation == True): output_messagetitle = output_messagetitle + " (GIF)"

output_picturename = os.path.basename(output_picturepath)
file_extension = pathlib.Path(output_picturepath).suffix
if (file_extension == "gif"): output_picturemime = "image/gif"
elif (file_extension == "jpg"): output_picturemime = "image/jpeg"
else: output_picturemime = "application/unknown"

output_messagebody = output_messagebody + args.messagebody
#https://pushover.net/api#attachments
if (stats.st_size > cf['pushover']['maxattachmentsize']): output_messagebody = output_messagebody + ' (At ' + stats.st_size + " bytes, the attached video is too large for pushover's " + cf['pushover']['maxattachmentsize'] + " bytes limit and has therefore been replaced with the usual example image.)"

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
  "attachment": (output_picturename, open(output_picturepath, "rb"), output_picturemime)
})

if (args.keepanimation == False and output_picturepath != scriptfolder + "/" + cf['exampleanimation'] ):  os.remove(output_picturepath)

if args.verbose == True: 
    print(r.text)
    print (output_picturepath)
