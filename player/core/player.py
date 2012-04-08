import subprocess, config, os
from threading import Timer

class Player:
	def __init__(self):
		self.startedTime = 1
		self.onStartedFn = False
		self.startedTimer = Timer(self.startedTime, self.onStarted);

	def play_file(self, filename):
		try:
			subprocess.Popen(config.player_path + " " + filename, shell=True);
		except:
			print "Failed to play file: " + str(filename)
	
	def onStarted(self, fn):
		self.onStartedFn = fn
		self.onStartedCheck()
	
	def onStartedCheck(self):
		if os.popen("ps xa|grep mplayer|grep -v grep").read():
			if self.onStartedFn:
				self.onStartedFn()
			return
		self.startedTimer.cancel();
		self.startedTimer = Timer(self.startedTime, self.onStartedCheck);
		self.startedTimer.start()
