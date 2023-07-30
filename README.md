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
sudo pip3 install requests
```
and this tool itself:
```bash
cd /opt
sudo git clone https://github.com/Starwhooper/RPi-motionalert /opt/RPi-motionalert

```
## First configurtion ##
```bash
sudo cp /opt/RPi-motionalert/config.json.example /opt/RPi-motionalert/config.json
sudo nano /opt/RPi-motionalert/config.json
```
insert apikey and userkey for pushover and check the right folder

## Add to motionEye
Insert Command: python3 /opt/RPi-motionalert/alert.py -v -c 1 -t "%$" -p %Y-%m-%d/%H-%M-%S.jpg
* -v: mean verbose
* -c 1: means video device camera id on motionEye (not the camera id in motion itself)
* -t "%$": means the Cameraname
* -p %Y-%m-%d/%H-%M-%S.jpg: means the picture

# sources of knowledge:
* Animated example: https://www.animatedimages.org/img-animated-animal-image-0051-80826.htm
* python code: https://support.pushover.net/i44-example-code-and-pushover-libraries#python-image
* pushover parameter: https://pushover.net/api
* motion parameter: https://motion-project.github.io/motion_config.html#conversion_specifiers







## Start ##
add it to rc.local to autostart as boot
```bash
sudo nano /etc/rc.local
/opt/RPi-docscan/scan.py
```

## Update ##
If you already use it, feel free to update with
```bash
cd /opt/RPi-docscan
sudo git pull origin main
```

## Hardware ##
### Case ###
Case to enclosure Raspberry Pi zero ans Waveshare 1.44inch LCD HAT_ https://www.thingiverse.com/thing:5324460
