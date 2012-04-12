import json, socket, config, sys

class Apiclient:
	def getSeries(self):
		ans = self.sendData({"cmd" : "getseries"})
		if not ans:
			return []
		return ans

	def getSeasons(self, media_id):
		ans = self.sendData({"cmd" : "getseasons", "id" : media_id})
		if not ans:
			return []
		return ans

	def getEpisodes(self, media_id, season):
		ans = self.sendData({"cmd" : "getepisodes", "id" : media_id, "season" : season})
		if not ans:
			return []
		return ans

	def getMovies(self):
		ans = self.sendData({"cmd" : "getmovies"})
		if not ans:
			return []
		return ans

	def getMoviePoster(self, media_id):
		ans = self.sendData({"cmd" : "getmovieposter", "id" : media_id}, False)
		if not ans:
			return ""
		return ans

	def sendData(self, data, retJson = True):
		ip = ""
		port = ""
		if config.mode == "master":
			ip = config.ip
			port = config.port
		else:
			ip = config.server_ip
			port = config.server_port
		try:
			s = socket.socket() 
			s.connect((ip, port))
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
			print "Could not connect to server " + str(ip) + ":" + str(port) + "..."
			return False

	def resync(self):
		self.sendData({"cmd" : "resync"})
