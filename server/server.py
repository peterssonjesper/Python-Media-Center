import sys, os, getopt, config
from threading import Thread

working_folder = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.insert(0, working_folder + "/server/core")

from api import *
from db import *
from sync import *
from classifier import *
from collector import *

if config.dynamicWatch:
  from watcher import *

class Server(Thread):
  def __init__(self):
    Thread.__init__(self)
  def run(self):
    db = Db()
    classifier = Classifier()

    s = Sync(db, classifier)

    if config.initsync:
      print "Doing initial sync..."
      s.initSync()
      print "Initial syncing done!"

    if config.dynamicWatch:
      print "Launching watcher deamon"
      watcher = Watcher(classifier, db)

    print "Starting collector..."
    collector = Collector()
    collector.start()

    print "Starting server at " + str(config.ip) + ":" + str(config.port)
    api = Api(db, s)

    print "Now listening..."
    api.start()

    db.disconnect()
