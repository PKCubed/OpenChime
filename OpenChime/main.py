"""OpenChime - the open source school bell system"""
# Created and maintained by Peter Kyle (PK Cubed)
# https://github.com/PKCubed/OpenChime


status = "starting"
enable_notifications = True


"""
LED Codes:

on					running
off					off
slow blink			starting
fast blink			error
blink off				bell
Long on, Short off		USB disconnected
"""

flask_port = 5050
verbose_enabled = True

import os
import time
import threading

def led_init():
	os.system("echo none >/sys/class/leds/ACT/trigger")

def led_on():
	os.system("echo 1 >/sys/class/leds/ACT/brightness")

def led_off():
	os.system("echo 0 >/sys/class/leds/ACT/brightness")

led_init()

def led_thread_func(): # Function to control green status led
	global status
	while True:
		if status == "running": # Running
			led_on()
		elif status == "starting": # Starting
			led_on()
			time.sleep(1)
			led_off()
			time.sleep(1)
		elif status == "bell": # When a bell is rung
			led_off()
			time.sleep(0.5)
			status = "running" # Return to running
		elif status == "disconnected": # USB Drive disconnected
			led_on()
			time.sleep(1)
			led_off()
			time.sleep(0.25)
		elif status == "error": # Error
			led_on()
			time.sleep(0.25)
			led_off()
			time.sleep(0.25)
		else: # Not running, or other
			led_off()

# Start led control thread
led_thread = threading.Thread(target=led_thread_func, daemon=True)
led_thread.start()




start_duration = 15 # The number of seconds to wait before playing any sounds while the program starts up

def log(text): # Log a message to the log files and print to terminal
	try:
		print(str(text))
		with open("log.txt", "a") as f:
			f.write(str(text) + "\n")
			f.close()
			os.system("cp log.txt usb/log.txt")
	except:
		log("Error with log function")

def verbose(text):
	if verbose_enabled:
		log(str(text))
	

with open("log.txt", 'r+') as f: # Clear Log file
    f.truncate(0)
    f.close()
		
log("---")
log("OpenChime v0.1 Starting...")

start_time = time.time() # Set the start time
log("Start Time: " + str(start_time))

log("verbose="+str(verbose_enabled))
verbose("Verbose mode is active. More detail will be logged.")



usb_drive_name = "OPENCHIME" # The name of the usb drive partition
verbose(f"USB drive should be named {usb_drive_name}")
usb_mount_location = "/home/openchime/OpenChime/usb" # The location for the usb drive to be mounted
usb_init_files_location = "/home/openchime/OpenChime/usb_init" # The location of the files to be transfered to the usb drive
audio_files = []

enable_webui = False
flask_running = False


import pyudev
import subprocess
import json
import datetime
from ics import Calendar, Event
import arrow
import icalendar
import recurring_ical_events

import urllib.request as urllib2

verbose("Succesful import of main libraries")


def wav(path): # Play a wave file
	verbose("wav " + str(path))
	output = os.system("aplay " + path)
	verbose(output)

def play(sound): # Play a local file in a new thread
	verbose("Play sound " + str(sound))
	if enable_notifications:
		x = threading.Thread(target=wav, args=("audio/"+sound+".wav",))
		x.start()
		log("Playing sound: " + sound)
	
play("startup")

calendar_link = "" # This is set in the usb config.json file
c = None
ics_text = None



last_bell = None
next_bell = None



last_refresh = time.time()
refresh_interval = 86400 # Seconds


recursion_days = 7 # Only affects last bell and next bell in web gui. High numbers can slow down processing.



last_bell_value = 1440 # Minutes



def get_net_interfaces():
	interface_paths = ["eth0", "wlan0"]
	interface_path = "/sys/class/net/"
	interfaces = []
	for interface in interface_paths:
		try:
			f = open(interface_path+interface+"/operstate")
			text = f.read()
			f.close()
			if "up" in text:
				interfaces.append(interface)
		except:
			pass
	return interfaces

verbose("Succesful definition of function get_net_interfaces")

def setup_wifi(ssid, password):
	log("Configuring wifi network with ssid: '"+ssid+"' and password: '"+password+"'") 
	wpa_supplicant = "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\n\n"
	wpa_supplicant += 'network={\n    ssid="'+ssid+'"\n    psk="'+password+'"\n}'
	f = open("/etc/wpa_supplicant/wpa_supplicant.conf","w")
	f.write(wpa_supplicant)
	f.close()
	log("Connecting to wifi")
	os.system("wpa_cli -i wlan0 reconfigure")

verbose("Succesful definition of function setup wifi")

def get_recursions(c, ics_text):
	days = recursion_days

	now = datetime.datetime.fromtimestamp(time.time())
	min_obj = now - datetime.timedelta(days=days)
	max_obj = now + datetime.timedelta(days=days)
	min_date = (min_obj.year, min_obj.month, min_obj.day)
	max_date = (max_obj.year, max_obj.month, max_obj.day)

	calendar = icalendar.Calendar.from_ical(ics_text)
	events = recurring_ical_events.of(calendar).between(min_date, max_date)

	for event in events:
		e = Event()
		e.begin = event["DTSTART"].dt
		e.end = event["DTEND"].dt
		e.name = event["SUMMARY"]
		c.events.add(e)

	return c

verbose("Succesful definition of function get_recursions")

def refresh():
	global last_refresh
	global next_bell
	global last_bell
	global c
	global ics_text
	c, ics_text = get_calendar(calendar_link)

	if c and ics_text:
		c = get_recursions(c, ics_text)	
	
		next_bell = get_next_bell(c)
		last_bell = get_last_bell(c)

	else: 
		next_bell = "None"
		last_bell = "None"

	last_refresh = time.time()

verbose("Succesful definition of function refresh")

def get_calendar(url):
	if url:
		log("fetching calendar from url")
		cmdoutput = os.system("wget -O schedule.ics "+url)
		verbose(cmdoutput)
		with open("schedule.ics", 'r') as file:
			ics_text = file.read()
		try:
			c = Calendar(ics_text)
			verbose("Calendar retrieved successfully")
			return c, ics_text
		except:
			log("Error retrieving calendar")
			return None, None
	else:
		log("No url for calendar specified. Please get a Google Calender ICAL link and put it in the configuration file on usb drive")
		return None, None

verbose("Succesful definition of function get_calendar")

def internet_on():
    try:
        urllib2.urlopen('http://google.com', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False

verbose("Succesful definition of function internet_on")

def get_ip():
	ip = subprocess.check_output("hostname -I", shell=True).decode("utf-8")[:-1]
	log("IP Address = " + ip)
	return ip

verbose("Succesful definition of function get_ip")

# Flask web interface initialization
from flask import Flask, request, render_template, jsonify, redirect
app = Flask(__name__)
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
from werkzeug.security import generate_password_hash, check_password_hash

verbose("Succesful import of flask libraries")

flask_user = 'admin'
flask_pw = '1234'
users = {
	flask_user: generate_password_hash(flask_pw)
}
def set_flask_user(pw):
	global flask_user
	global users
	users = {
		flask_user: generate_password_hash(pw)
	}
	
verbose("Succesful definition of function set_flask_user")

# Flask pages

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route('/', methods=['GET', 'POST']) # Modifies the behavior of the index function.
# No login required for index
# @auth.login_required
def index():
	now = datetime.datetime.now()
	web_time = now.strftime("%H:%M:%S")
	return render_template("index.html", web_time=web_time, audio_files=audio_files)

@app.route("/buttons", methods=['GET', 'POST'])
@auth.login_required
def button():
	now = datetime.datetime.now()
	web_time = now.strftime("%H:%M:%S")
	if request.method == 'POST':
		if request.form['submit_button'] == 'Manual Bell':
			chime = request.form['audio_file_dropdown']
			log("Web UI - Manual bell ("+chime+")")
			ring(chime)
		elif request.form['submit_button'] == 'Refresh':
			log("Web UI - Resfresh button pressed")
			refresh()
		else:
			log("Web UI - Unknown button")
	return redirect("/", code=302)

@app.route("/update", methods=['GET', 'POST'])
@auth.login_required
def update():
	now_seconds = time.time()
	now = datetime.datetime.now()
	ip_address = get_ip()
	if internet_on():
		internet_status = "Connected"
		con_type = " ".join(get_net_interfaces())
	else:
		internet_status = "Not Connected"
		con_type = "None"
	return jsonify({
	   'time': now.strftime("%H:%M:%S"),
	   'uptime': str(datetime.timedelta(seconds=round(now_seconds-start_time))),
	   'status': status,
	   'internet_status': internet_status,
	   'ip_address': ip_address,
	   'con_type': con_type,
	   'last_bell': last_bell,
	   'next_bell': next_bell
	})

verbose("Succesful definition of flask pages")

def flask_thread_func():
	if __name__ == "__main__":
		app.run(host="0.0.0.0", port=flask_port)

flask_thread = None
def run_flask():
	global flask_thread
	global flask_running
	if not flask_running:
		flask_thread = threading.Thread(target=flask_thread_func, daemon=True)
		flask_thread.start()
		flask_running = True

def stop_flask():
	global flask_thread
	global flask_running
	flask_thread._stop()
	flask_running = False

verbose("Succesful init of flask")

status = "Good"

def get_next_bell(c):
	if list(c.timeline.start_after(arrow.get(time.time()))):
		next_bell = list(c.timeline.start_after(arrow.get(time.time())))[0].begin
		return next_bell.datetime.strftime("%m/%d/%Y, %H:%M:%S")

	return None # If there is not a bell in the future

def get_last_bell(c):
	now = arrow.get(time.time())
	global last_bell_value
	for i in range(last_bell_value):
		then = now.shift(minutes=-i)
		if list(c.timeline.at(then)):
			last_bell = list(c.timeline.at(then))[0].begin
			return last_bell.datetime.strftime("%m/%d/%Y, %H:%M:%S")

	return None # If the last bell was too long ago, or didn't happen at all



def ring(sound): # Play a remote/usb file in a new thread
	x = threading.Thread(target=wav, args=(usb_mount_location+"/"+sound+".wav",))
	x.start()
	log("Playing sound: " + sound)

def usb_init(usb_loc,mnt_loc): # Initialize the USB drive
	os.system("sudo umount "+mnt_loc) # Make sure drive is not already mounted
	try:
		os.system("sudo mount -o umask=0022,gid=1000,uid=1000 "+usb_loc+" "+mnt_loc) # Mount the drive
		success = True # If drive was mounted, success!
	except:
		log("USB drive at " + usb_loc + " mount to: " + mnt_loc + " failed. USB drive not mounted.") # If drive was unable to mount
		success = False

	if success: # If mounting was successful
		files_moved = 0
		usb_files = subprocess.check_output("ls " + mnt_loc, shell=True).decode("utf-8").split("\n")[:-1] # Get files on usb drive
		usb_init_files = subprocess.check_output("ls " + usb_init_files_location, shell=True).decode("utf-8").split("\n")[:-1] # Get init files to put on usb drive
		log("usb_files = " + str(usb_files))
		log("usb_init_files = " + str(usb_init_files))
		for i in usb_init_files: # For each init file/folder,
			if i not in usb_files: # If that file/folder is not on the drive,
				files_moved += 1
				os.system("sudo cp "+usb_init_files_location+"/"+i+" "+mnt_loc+"/"+i) # Copy that file/folder from the init folder to the usb drive.
				log("Copied file "+i+" to usb drive as it is required but didn't exist.")
		if files_moved == 0: # If no files were copied to the drive
			log("USB Drive has all required files")

		usb_files = subprocess.check_output("ls " + mnt_loc, shell=True).decode("utf-8").split("\n")[:-1] # Get files on usb drive again (after initialization)
			
		audio_files = []
		# Get a list of all audio files.
		for i in usb_files:
			if i[-4:] == ".wav":
				audio_files.append(i[:-4])

		print("Audio files on drive: " + str(audio_files))

		return True, audio_files

	return success, None # Return the success variable to indicate to the main loop whether mouning was successful.

def usb_load(mnt_loc): # Load config and schedule files from usb
	verbose("Starting usb_load function")
	# Open config file
	with open(mnt_loc + "/config.json") as json_file: # Open config file
		json_file = json_file.read().replace("'", '"') # Set all single quotes to double quotes
		data = json.loads(json_file) # Load json data into a dict
		for i in data:
			if data[i] == "True" or data[i] == "true": # Set true to true and false to false
				data[i] = True
			elif data[i] == "False" or data[i] == "false":
				data[i] = False
		config = data # Set the config variable to the config data
		log("Config successfully loaded")
		log(str(data))

	return config # Return both config and schedule to the main loop.

verbose("Succesfully defined main functions, continuing on to main loop")

usb_connected = False
usb_connected_sound = None
usb_ready = False
usb_success = False

chime = "Bell"

last_stamp = None
last_usb_update = int(time.time())

context = pyudev.Context() # Set the context for pyudev which is used to read partitions

verbose("Sleeping for 5 seconds")

time.sleep(5)

# Main loop
while True:
	time.sleep(1)
	# Get partitions and their locations to mount from
	if int(time.time()) >= last_usb_update + 1:
		partitions = {}
		partition_names = []
		last_usb_update = int(time.time())
		devices = context.list_devices(subsystem='block', DEVTYPE='partition')
		if verbose:
			print("USB Device Check: List devices")
			print(devices)
		for device in devices:
		    partition_names.append(device.get('ID_FS_LABEL', 'unlabeled partition'))
		    partitions[device.get('ID_FS_LABEL', 'unlabeled partition')] = device.device_node
		if verbose:
		    print(partition_names)
		    print(partitions)
		print("Usb Device List Refreshed")
		    
	if usb_drive_name in partition_names: # If usb drive is connected and recognized
		print("USB Drive Detected")
		usb_drive_location = partitions[usb_drive_name] # Get the location of the drive
		if not usb_connected: # If usb drive was not connected before
			log("USB Drive Connected")
			status = "running"
			usb_connected = True
			usb_success, audio_files = usb_init(usb_drive_location, usb_mount_location) # Mount and initialize the usb drive
			config = usb_load(usb_mount_location) # Load data from usb drive
			ssid = config["wifi_ssid"] # Get wifi ssid 
			password = config["wifi_password"] # Get wifi password
			enable_webui = config["enable_webui"] # Get webui enable/disable
			calendar_link = config["google_calendar_url"] # Get google calendar url
			flask_pw = config["webui_password"] # Get webui password
			set_flask_user(flask_pw) # Set webui password
			enable_notifications = config["notifications"]
			if ssid: # If ssid is not blank,
				setup_wifi(ssid, password) # connect to wifi
			refresh() # Refresh the calendar
			log("USB Drive Loaded")
		if usb_connected_sound != True:
			now = time.time() # Get the current timestamp
			if now >= start_time + start_duration: # If now is after the start_duration
				if usb_success: # If usb initialization and config was successful
					log("USB Drive at " + usb_drive_location + " mounted to: " + usb_mount_location)
					log("USB Drive Initialization Successful")
					play("usb_connect") # Play usb_connect sound
					time.sleep(5)
					usb_ready = True
				else: # If usb initialization and config failed.
					log("USB Drive Initialization Failed.")
					play("error") # play error sound
					status = "error"
				usb_connected_sound = True
		
	elif not usb_drive_name in partition_names: # If usb drive is not connected
		print("USB Drive not detected")
		status = "disconnected"
		if usb_connected: # If usb drive was connected before
			usb_connected = False
			usb_success = False
			usb_ready = False
			audio_files = []
		if usb_connected_sound != False:
			now = time.time()
			if now >= start_time + start_duration:
				if usb_connected_sound == None:
					log("USB Drive Not Connected")
				else:
					log("USB Drive Disconnected")
				play("usb_disconnect")
			usb_connected_sound = False

	if usb_ready: # If the usb is set up and ready to go'
		status = "running"
		if enable_webui:
			run_flask() # Start the flask web interface
		else:
			stop_flask()
		
		stamp = time.time() # Get the current timestamp in epoch seconds (since 1970)
		min_stamp = int(stamp/60) # Get the current timestamp in epoch minutes (since 1970) and truncate it to the nearest minute

		bells = [] # Set bells list
		if c:
			for i in c.timeline.at(arrow.get(time.time())): # for each bell that is occuring NOW
				bells.append(i) # append each bell to the bells list
			if bells: # If the bells list is not empty (there are bells occuring now)
				bell = bells[0].name # Get the name of the first bell in the list
			else: # Else, if there are no bells in the list
				bell = None # Set the bell variable to none
				
			if last_stamp != min_stamp: # if we haven't already rung the bell this minute
				if bell: # If a bell is occuring
					last_stamp = min_stamp # Set the the last_stamp to the current minute stamp
		
					log("Triggered on " + str(time.ctime(time.time())) + " with sound file " + str(bell)) # Log that we triggered a bell
					status = "bell"
					ring(bell) # Ring with the specified sound file on usb.
				next_bell = get_next_bell(c)
				last_bell = get_last_bell(c)

	# If haven't refreshed the calender in at least one day or another refresh interval
	if time.time() - last_refresh >= refresh_interval:
		refresh() # Refresh (get calender and calculate recursions)
			