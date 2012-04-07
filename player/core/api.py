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

	def getMetadata(self, media_id):
		return self.sendData({"cmd" : "getmetadata", "media_id" : media_id})

	def getPoster(self, media_id):
		return self.sendData({"cmd" : "getposter", "media_id" : media_id}, False)

	def sendData(self, data, retJson = True):
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
			if retJson:
				return json.loads(ans)
			else:
				return ans
		except:
			print "Could not connect to server..."
			return False

	def resync(self):
		self.sendData({"cmd" : "resync"})
