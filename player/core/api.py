import json, socket, config, sys

class Api:
	def getSeries(self):
		return self.sendData({"cmd" : "getseries"})

	def getSeasons(self, media_id):
		return self.sendData({"cmd" : "getseasons", "media_id" : media_id})

	def getEpisodes(self, media_id, season):
		return self.sendData({"cmd" : "getepisodes", "media_id" : media_id, "season" : season})

	def getMovies(self):
		return self.sendData({"cmd" : "getmovies"})

	def sendData(self, data):
		try:
			s = socket.socket() 
			s.connect((config.server_ip, config.server_port))
			s.send(json.dumps(data))
			ans = ""
			while True:
				tmp = s.recv(1024)
				if not tmp:
					break
				ans = ans + tmp 
			s.close()
			return json.loads(ans)
		except:
			print "Could not connect to server..."
			return False

	def resync(self):
		self.sendData({"cmd" : "resync"})