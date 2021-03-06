import os
import config
import pyinotify

class Watcher:

  def __init__(self, classifier, db):
    self.wm = pyinotify.WatchManager()
    self.mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE
    for watchDir in config.watchDirs:
      self.wm.add_watch(watchDir, self.mask, rec=True, auto_add=True)

    self.notifier = pyinotify.ThreadedNotifier(self.wm, self.EventHandler(classifier, db, self.wm))
    self.notifier.start()

  class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, classifier, db, wm):
      self.classifier = classifier
      self.db = db
      self.wm = wm
    def process_IN_CREATE(self, event):
      type = self.classifier.getType(event.path, event.name)
      if not(event.dir) and type > 0:
        base_dir = [watchDir for watchDir in config.watchDirs if (watchDir in event.path)][0]
        inner_dir = event.path.replace(base_dir,'')
        dirName = event.path.split("/")[-1];
        info = self.classifier.getInfo(dirName, event.pathname, type)
        data = {
        "title" : info[0],
        "base_dir" : base_dir,
        "inner_dir" : inner_dir,
        "filename" : event.pathname,
        "media_type" : type,
        "season" : info[1],
        "episode" : info[2],
        "failbit" : info[3]
        }
        self.db.insert_file(data)
        print "Inserted ", info[0], info[1], info[2]
    def process_IN_DELETE(self, event):
      type = self.classifier.getType(event.path, event.name)
      if not(event.dir) and type > 0:
        self.db.delete_file(event.pathname)
        print "Deleted ", event.pathname
