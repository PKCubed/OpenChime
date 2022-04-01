# OpenChime
An open source Raspberry Pi based school bell system.

I started work on this project after I learned how expensive and limited the systems availible are.

OpenChime uses Google Calendar as well as a web interface to allow easy live control of the bell system and schedule. Because the bell system simply links to a Google Calendar, you can share the schedule with other people for them to view or edit. You can edit the schedule any time, and either reboot the system, or press refresh on the web user interface to update the schedule. A usb drive must also be connected. It does not need to be very large as all it does is store the audio files, configuration, and log file. Incase a problem occurs, the log file lists everything that has happened including when bells have rung, and any errors that have occured.

OpenChime uses ntp, or network time protocal, for accurate time. If you have a clock system or light system that uses ntp or gps time, OpenChime should sync with those systems increadibly well. If it does not, and you would like them to sync up, you can edit the time offset in seconds in the config file on the usb drive.

OpenChime allows you to use as many custom sounds as you want. Just load any .wav file onto the usb drive and setup an event in Google Calendar with the name of the bell file (without the .wav) as the name of the event. A description is optional.

OpenChime connects with either ethernet (recomended) and/or wifi. If you connect an ethernet cable to OpenChime, it should automatically connect. When using wifi, you will need to specify the ssid and password in the config file on the usb drive.



## Before you start

I, the creater of OpenChime, am happy to help you solve any problems you have. Email me at peterdooga@gmail.com, or join my discord server, https://discord.gg/ZqP9ERJ.

This project is not yet  released and is not guarenteed to work on every device.

Tips:
When using linux and some software (such as snowflake ssh), use ctrl+shift+x, ctrl+shift+c, and ctrl+shift+v instead of ctrl+x, ctrl+c, and ctrl+v

## Install instructions:

Download the openchime_v1.0.img file and flash it onto an SD card using software like Etcher. Put the card into a Raspberry Pi from the supported Pis list.

Plug your Raspberry Pi into ethernet, or use wifi with either a wifi dongle or the built in wifi on newer Pis. For wireless connectivity, you need to set the wifi ssid and password with the configuration file on the usb drive. We'll get to that later.

Plug your speakers or other audio device into the pi's audio jack. This is where the bell or other sounds will be outputted.

Finally, you will need a USB drive. The USB drive should be of an equal or greater size than 1gb, but small enough that you can format it with vfat or fat32. Format the drive with fat32.

Eject and remove the USB drive from the computer. Then plug the drive into the Pi and make sure that it is the only storage device pluged in. You should only have it and possibly a wifi dongle connected.

Finaly, plug the Raspberry Pi into power. It will create some files on the USB drive. OpenChime will play it's startup sound, and the green light will blink slowly. This means that it is starting up. When its done, it will play another sound and the green light will be solid. You can then unplug the USB drive and plug it back into your computer. We need to now edit the config file as well as set the schedule link. We'll start with the config. The config file has a few options. One thing you may want to change is the notifications setting. This enables or disables the sounds triggered by certain events such as on boot or when the USB drive is pluged in or unpluged. By default, this should be set to True. Howver, you may want to set it to False. Don't forget to capitalize True and False. This is also where you configure the wifi ssid (name) and password.

The schedule link also needs to be changed. By default, the schedule link is blank. To get your Google Calendar link and add it to OpenChime, you need to first create a Calendar, or, if you already have one, you can use it. Then, click on the 3 dots next to the calendar on the left bar on the main screen of Google Calendar. Then click on "Settings and sharing". You can find the ICAL link at the bottom of the calendar settings page that opens. You can copy either the public ICAL link or the private ICAL link. Both will work, but the public ICAL link requires you to make the Calendar public.

The last thing we need to change is the web user interface password, or webui password. If you do not want or do not need a web user interface, you can disable it in the config as well. It is enabled by default. The web interface allows you to view information from OpenChime, as well as manually ring a bell or refresh the calendar.

Note:
OpenChime will ring at the start of each minute for each event, (when the second hand hits 12 on an anolog clock).



LED Codes:

on					running
off					off
slow blink			starting
fast blink			error
blink off				bell
Long on, Short off		USB disconnected



## Troubleshooting and Help

For help with anything related to OpenChime, you can post an issue on the github page, join the discord server, or email me. (peterdooga@gmail.com)



## Tested Computers and Micro Computers

Raspberry Pi 2b

