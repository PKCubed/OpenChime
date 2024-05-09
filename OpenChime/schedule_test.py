"""
stamp = time.time()
		min_stamp = round(stamp/60)

		bells = []
		for i in c.timeline.now():
			bells.append(i)
		if bells:
			bell = bells[0].name
		else:
			bell = None
		
		if bell and last_stamp != min_stamp:
			last_stamp = min_stamp

			log("Triggered at " + str(stime) + " with sound file " + str(chime))
			ring(chime) # Ring with the specified sound file on usb.		
"""





import os
import time
from ics import Calendar, Event
import datetime
import icalendar
import recurring_ical_events

cal_url = "https://calendar.google.com/calendar/ical/152pb7gadctthtdt7jq161gp9c%40group.calendar.google.com/private-240038f12f111a03d31986485edfbe2e/basic.ics"

os.system("wget -O schedule.ics "+cal_url)

with open("schedule.ics", 'r') as file:
	ics_text = file.read()

start_date = (2021,10,1)
end_date = (2021,11,1)

calendar = icalendar.Calendar.from_ical(ics_text)
events = recurring_ical_events.of(calendar).between(start_date, end_date)

c = Calendar()

for event in events:
	name = event["SUMMARY"]
	print(name)
	start = event["DTSTART"].dt
	print(start)
	end = event["DTEND"].dt
	print(end)
	e = Event()
	e.begin = start
	e.end = end
	e.name = name
	c.events.add(e)

print(c)

def get_recursions(c, ics_text):
	days = 7

	now = datetime.datetime.fromtimestamp(time.time())
	min_obj = now - datetime.timedelta(days=days)
	max_obj = now + datetime.timedelta(days=days)
	min_date = (min_obj.year, min_obj.month, min_obj.day)
	max_date = (max_obj.year, max_obj.month, max_obj.day)

	calendar = icalendar.Calendar.from_ical(ics_text)
	events = recurring_ical_events.of(calendar).between(start_date, end_date)

	for event in events:
		e = Event()
		e.begin = event["DTSTART"].dt
		e.end = event["DTEND"].dt
		e.name = event["SUMMARY"]
		c.events.add(e)
































































