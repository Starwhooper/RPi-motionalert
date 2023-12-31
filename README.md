send alerts during motion

# RPi-motion-alert

optimized to use motion, motioneye or motioneyeos with pushover, include images/animated images

Main features:
* support pushover
* create animated gif
* support animated gif with pushover

## Installation ##
install all needed packages to prepare the software environtent of your Raspberry Pi:

```bash
sudo pip3 install requests python-ffmpeg
```
and this tool itself:
```bash
cd /opt
sudo git clone https://github.com/Starwhooper/RPi-motionalert /opt/RPi-motionalert

```
## First configurtion ##
```bash
sudo cp /opt/RPi-motionalert/config.example.json /opt/RPi-motionalert/config.json
sudo nano /opt/RPi-motionalert/config.json
```
insert apikey and userkey for pushover and check the right folder

## Add to motionEye
Insert Command to "Actions when motion has startet": python3 /opt/RPi-motionalert/alert.py -v -c 1 -t "%$" -p %Y-%m-%d/%H-%M-%S.jpg
* -v: means verbose
* -c 1: means video device camera id on motionEye (not the camera id in motion itself)
* -t "%$": means the Cameraname
* -p %Y-%m-%d/%H-%M-%S.jpg: means the picture

Insert Command to "Actions when motion has ended": python3 /opt/RPi-motionalert/alert.py -v -a -c 1 -t "%$" -p %Y-%m-%d/*.avi
* -v: means verbose
* -a: means to convert videofile in animated gif
* -c 1: means video device camera id on motionEye (not the camera id in motion itself)
* -t "%$": means the Cameraname
* -p %Y-%m-%d/*.avi: means the videos, beware to set the right extension


## Update ##
If you already use it, feel free to update with
```bash
cd /opt/RPi-motionalert
sudo git pull origin main
```

# sources of knowledge:
* Animated example: https://www.animatedimages.org/img-animated-animal-image-0051-80826.htm
* python code: https://support.pushover.net/i44-example-code-and-pushover-libraries#python-image
* pushover parameter: https://pushover.net/api
* motion parameter: https://motion-project.github.io/motion_config.html#conversion_specifiers
* python ffmpeg: https://pypi.org/project/python-ffmpeg/
