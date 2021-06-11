## OpenChime
An open source Raspberry Pi based school bell system.

I started work on this project after I learned how expensive and limited the systems on the market right now are.

OpenChime allows you to configure the schedule, sounds, and other settings. All the config files are stored on a usb drive. A list of options can be found below.



# Install instructions:

Download the openchime_v0.1.img file and flash it onto an SD card. Put the card into a Raspberry Pi from the supported Pis list.

Plug your Raspberry Pi into ethernet, or use wifi with either a wifi dongle or the built in wifi on newer Pis. For wireless connectivity, you need to set the wifi ssid and password with the chimeconfig usb drive. We'll get to that later.

Plug your speakers or other audio device into the pi's audio jack. This is where the bell or other sounds will be outputted.

Finally, you will need a USB drive. The USB drive should be of a greater size than 1mb, but small enough that you can format it with vfat or fat32. Format the drive with fat32. Before you plug the drive into the pi, you need to add a file to it.

Plug the drive into a computer. Create a text file on the drive titled wifi.json. Set the contents to this and make sure to replace the ssid and password with your wifi's credentials.
`
{
"ssid":"replace this text with your ssid",
"pswd":"replace this text with your password"
}
`
Save the file then eject and remove the USB drive from the computer. Then plug the drive into the Pi and make sure that it is the only storage device pluged in. You should only have it and possibly a wifi dongle connected.

Finaly, plug the Raspberry Pi into power. It will create some files on the USB drive. When its done, it will play a tone. You can then unplug the USB drive and plug it back into your computer. We need to now edit the config file as well as set the schedule. In the current version, you have to type out the schedule manually, but its not too hard. We'll start with the config. The config file has many options. They all should be changed similar to the way you may have changed the wifi.json file to configure the wifi credentials. One thing I'll change is the notifications setting. This enables or disables the chimes triggered by certain events such as on boot or when the USB drive is pluged in or unpluged. By default this should be set to False. I'll set it to True though. Don't forget to capitalize True and False.

`
"notifications":True,
`

The schedule also needs to be edited. By default, the schedule is blank. The file will look like this:

`
{

}
`

To set the bell to ring at a certain time, we need to first choose a day, then choose the times the bell should ring on that day. For example, if we wanted the bell to ring at 12:00 pm on Monday, we edit the config file to look like this.

`
{
"mon":["1200"]
}
`

As you can see, we define a list of times on monday, or mon. those times are abreviated with 24 hour time. We also remove the colon. So for example, 1:30 pm would be "1330", and 8:54 am would be "0854".

OpenChime will ring at the start of each minute, (when the second hand hits 12).



# Tested Raspberry Pis

Raspberry Pi 2b

