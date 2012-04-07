import sys, os, inspect, getopt, config

run_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])
sys.path.insert(0, run_folder + "/core")

from api import *
from db import *
from sync import *
from classifier import *
from collector import *

if __name__ == "__main__":
	initSync = True
	startServer = True
	startCollector = True
	try:
		opts, args = getopt.getopt(sys.argv[1:], "", ["no-initsync", "no-server", "no-collector"])
		for o, a in opts:
			if o == "--no-initsync":
				initSync = False
			if o == "--no-server":
				startServer = False
			if o == "--no-collector":
				startCollector = False
	except:
		print "Unknown flag specified.\nUsage: main.py [--no-initsync] [--no-server] [--no-collector]"
		sys.exit(0)

	db = Db()
	classifier = Classifier()

	s = Sync(db, classifier)

	if initSync:
		print "Doing initial sync..."
		s.initSync()
		print "Initial syncing done!"

	if startCollector:
		print "Starting collector..."
		collector = Collector()
		collector.start()

	if startServer:
		print "Starting server at " + str(config.hostname) + ":" + str(config.port)
		api = Api(db, s)

		print "Now listening..."
		api.start()

	db.disconnect()
