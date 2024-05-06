# OpenChime
An open source Raspberry Pi based school bell system.

I started work on this project after I learned how expensive and limited the systems availible are.

OpenChime uses Google Calendar as well as a web interface to allow easy live control of the bell system and schedule. Because the bell system simply links to a Google Calendar, you can share the schedule with other people for them to view or edit. You can edit the schedule any time, and either reboot the system, or press refresh on the web user interface to update the schedule. A usb drive must also be connected. It does not need to be very large as all it does is store the audio files, configuration, and log file. Incase a problem occurs, the log file lists everything that has happened including when bells have rung, and any errors that have occured.

OpenChime uses ntp, or network time protocal, for accurate time. If you have a clock system or light system that uses ntp or gps time, OpenChime should sync with those systems increadibly well.

OpenChime allows you to use as many custom sounds as you want. Just load any .wav file onto the usb drive and setup an event in Google Calendar with the name of the bell file (without the .wav) as the name of the event. A description is optional.

OpenChime connects with either ethernet (recomended) and/or wifi. If you connect an ethernet cable to OpenChime, it should automatically connect. When using wifi, you will need to specify the ssid and password in the config file on the usb drive.



## Before you start

I, the creater of OpenChime, am happy to help you solve any problems you have. Email me at peterdooga@gmail.com, or join my discord server, https://discord.gg/ZqP9ERJ.

This project is not yet  released and is not guarenteed to work on every device.

Tips:
When using linux and some software (such as snowflake ssh), use ctrl+shift+x, ctrl+shift+c, and ctrl+shift+v instead of ctrl+x, ctrl+c, and ctrl+v

## Install instructions:

[INSTALL_INSTRUCTIONS.md](INSTALL_INSTRUCTIONS.md)



## Troubleshooting and Help

For help with anything related to OpenChime, you can post an issue on the github page, join the discord server, or email me. (peterdooga@gmail.com)

LED Codes:

on - running, 
off - off, 
slow blink - starting, 
fast blink - error, 
blink off - bell, 
Long on Short off - USB disconnected



## Tested Computers and Micro Computers

Raspberry Pi 4b

