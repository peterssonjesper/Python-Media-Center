#!/usr/bin/python

import httplib, sys, json, os, inspect, time
run_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])
sys.path.insert(0, run_folder + "/core")

from db import *
from threading import Thread

class Collector(Thread):
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		db = Db()
		conn = httplib.HTTPConnection("www.imdbapi.com")

		while True:
			entry = db.getEntryWithoutMetadata()
			if not entry:
				time.sleep(60)
			else:
				title = entry[1]
				media_id = entry[0]
				search_string = title.replace(" ", "%20");
				print "Collecting data from IMDB: " + title
				conn.request("GET", "/?i=&t=" + search_string)
				r = conn.getresponse()
				json_data = r.read()
				try:
					data = json.loads(json_data)
					if 'ID' in data.keys():
						db.insertMetadata(media_id, data);
					else:
						db.updateMetadataId(media_id, -1)
				except:
					print "Could not parse answer for " + title

				db.commit()

		db.disconnect()
