## Before you start

I, the creater of OpenChime, am happy to help you solve any problems you have. Email me at peter@pkcubed.net.

This project is not released and is not guarenteed to work on every device.

Tips:
When using linux and some software (such as snowflake ssh), use ctrl+shift+x, ctrl+shift+c, and ctrl+shift+v instead of ctrl+x, ctrl+c, and ctrl+v

## Install OpenChime from image (Not Yet Available, instructions are inaccurate)
Download the openchime_v1.0.img or file or the latest version and flash it onto an SD card using software like Etcher. Put the card into a Raspberry Pi from the supported Pis list.

## Install OpenChime from source code
Download the OpenChime (Compressed).zip file and extract it onto a fresh install of Raspberry Pi OS with username "openchime". The OpenChime folder inside the zip file should be placed directly inside /home/openchime so that the main python file has the path /home/openchime/OpenChime/main.py.

In most cases you'll need to run this command to install packages with pip (change 3.11 to your version of python `python3 --version`):
`sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old`

Install dependencies:
- `pip install ics`
- `pip install icalendar`
- `pip install recurring_ical_events`
- `pip install flask` (Should be unneccesary on most Raspberry Pi OS installs)
- `pip install flask-httpauth`
- `pip install pyudev`

Run at Startup with Cron
`crontab -e`

paste the following lines at the end of the file:
```
XDG_RUNTIME_DIR=/run/user/1000
@reboot sleep 10 && sudo chown openchime:openchime /sys/class/leds/ACT -R && sudo chmod 777 /sys/class/leds/ACT -R && cd /home/openchime/OpenChime/ && sudo chown openchime:openchime usb -R && sudo chmod 777 usb -R && python3 main.py
# >> /home/openchime/OpenChime/cronlog.txt 2>&1
# uncomment the line above and add to the @reboot line to enable logging
```

We need to allow the python script to access the RPi LEDs. This is already handled by the crontab startup script, but we can do this in addition. Create a new file using the command below:
`sudo nano /etc/udev/rules.d/99-leds.rules`
then inside that file paste the following:
```
SUBSYSTEM=="leds", KERNEL=="ACT", ACTION=="add", RUN+="/bin/sh -c 'chgrp -R gpio /sys%p && chmod -R g+w /sys%p'"
```
You'll then need to save and exit the file, then reboot the raspberry pi with
`sudo reboot now`


## Setup and Config

Plug your Raspberry Pi into ethernet, or use wifi with either a wifi dongle or the built in wifi on newer Pis. For wireless connectivity, you need to set the wifi ssid and password with the configuration file on the usb drive. We'll get to that later.

Plug your speakers or other audio device into the pi's audio jack. This is where the bell or other sounds will be outputted.

Finally, you will need a USB drive. The USB drive should be of an equal or greater size than 1gb, but small enough that you can format it with vfat or fat32. Format the drive with fat32.

Eject and remove the USB drive from the computer. Then plug the drive into the Pi and make sure that it is the only storage device pluged in. You should only have it and possibly a wifi dongle connected.

Finaly, plug the Raspberry Pi into power. It will create some files on the USB drive. OpenChime will play it's startup sound, and the green light will blink slowly. This means that it is starting up. When its done, it will play another sound. You can then unplug the USB drive and plug it back into your computer. We need to now edit the config file as well as set the schedule link. We'll start with the config. The config file has a few options. One thing I'll change is the notifications setting. This enables or disables the sounds triggered by certain events such as on boot or when the USB drive is pluged in or unpluged. By default this should be set to True. I'll set it to False though. Don't forget to capitalize True and False. This is also where you configure the wifi ssid (name) and password.

The schedule link also needs to be changed. By default, the schedule link is blank. To get your Google Calendar link and add it to OpenChime, you need to first create a Calendar, or, if you already have one, you can use it. Then, click on the 3 dots next to the calendar on the left bar on the main screen of Google Calendar. Then click on "Settings and sharing". You can find the ICAL link at the bottom of the calendar settings page that opens. You can copy either the public ICAL link or the private ICAL link. Both will work, but the public ICAL link requires you to make the Calendar public.

The last thing we need to change is the web user interface password, or webui password. If you do not want or do not need a web user interface, you can disable it in the config as well. It is enabled by default. The web interface allows you to view information from OpenChime, as well as manually ring a bell or refresh the calendar.

Note: OpenChime will ring at the start of each minute for each event, (when the second hand hits 12).
