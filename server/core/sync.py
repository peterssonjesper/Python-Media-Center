import os
import config
from classifier import *

class Sync:
	def __init__(self, db, classifier):
		self.db = db
		self.classifier = classifier
	
	def initSync(self):
		self.db.erase()
		for watchDir in config.watchDirs:
			self.files_found = 0;
			if os.path.isdir(watchDir):
				self.recSync(watchDir, "")
			print "Found " + str(self.files_found) + " entries in " + watchDir
		self.db.commit()

	def recSync(self, base_dir, inner_dir):
		files = False
		try:
			files = os.listdir(base_dir + "/" + inner_dir)
		except:
			print "Could not sync directory " + base_dir + "/" + inner_dir + ", permission error?"
		if not files:
			return
		for f in files:
			if os.path.isdir(base_dir + "/" + inner_dir + "/" + f): # Directory
				if inner_dir == "":
					self.recSync(base_dir, f)
				else:
					self.recSync(base_dir, inner_dir + "/" + f)
			elif self.classifier.playable(base_dir + "/" + inner_dir + "/" + f, f): # Playable file
				type = self.classifier.getType(base_dir + "/" + inner_dir, f)
				if type > 0:
					dirName = inner_dir.split("/")[-1];
					info = self.classifier.getInfo(dirName, f, type)
					data = {
						"title" : info[0],
						"base_dir" : base_dir,
						"inner_dir" : inner_dir,
						"filename" : f,
						"media_type" : type,
						"season" : info[1],
						"episode" : info[2],
						"failbit" : info[3]
					}
					self.db.insert_file(data)
					self.files_found += 1
