import subprocess, config

class Player:
	def play_file(self, filename):
		try:
			subprocess.Popen(config.player_path + " " + filename, shell=True);
		except:
			print "Failed to play file: " + str(filename)
