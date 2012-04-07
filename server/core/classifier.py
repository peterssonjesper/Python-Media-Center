import os
import config
import re

class Classifier:
	def playable(self, full_path, filename):
		try:
			filename = filename.lower()
			ending = filename.split(".")[-1]
			is_part = True if re.search("part", filename) else False
			if ending in config.acceptedEndings and filename[0:1] != "." and (not is_part or filename[-6:] == "01.rar"):
				return True
		except:
			pass
		return False

	def getType(self, location, filename):
		try:
			dirName = location.split("/")[-1].lower()
			if self.isTv(dirName):
				return 1
			if self.isTvSeason(dirName):
				return self.getType(filename, "")
			if self.isMoviePack(dirName) and self.isMovie(dirName):
				return self.getType(filename, "")
			if self.isMovie(dirName):
				return 2
		except:
			pass
		return 0
	
	def isTv(self, s):
		if re.search("(s[0-9]{2})?[ed]p?[0-9]{2}\.|pdtv", s.lower()): # S01E01 format
			return True
		if re.search("\.[0-9]{1,2}x[0-9]{1,2}\.", s.lower()): # 1x01 format
			return True
		return False

	def isTvSeason(self, s):
		return True if re.search("s[0-9]{1,2}\.", s.lower()) else False
	
	def isMovie(self, s):
		return True if re.search("x264|vcd|svcd|xvid|divx|bluray|dvdr", s.lower()) else False

	def isMoviePack(self, s):
		return True if re.search("trilogy|quadriology|\.pack|septology|hexalogy|collection", s.lower()) else False
	
	def getInfo(self, dirName, filename, type):
		if self.isTvSeason(dirName) or self.isMoviePack(dirName): # Can't trust dirname, use filename
			dirName = filename

		name = dirName
		failbit = 0
		if type == 1: # TV
			res = re.search("(.*)\.(s[0-9]{2})?[ed]p?([0-9]{2})", dirName.lower()) # S01E01 format
			if not res:
				res = re.search("(.*)\.([0-9]{1,2})x([0-9]{1,2})\.", dirName.lower()) # 01x01 format
				if not res:
					failbit = 1
			try:
				res = res.groups()
				name = ""
				for s in res[0].split("."):
					name = name + s[0].upper() + s[1:] + " "
				name = name[:-1]

				season = ""
				if res[1] and res[1][0] == "s":
					season = res[1][1:]
				elif res[1]:
					season = res[1]

				episode = res[2]
				try:
					season = int(season)
				except:
					season = 1
				try:
					episode = int(episode)
				except:
					episode = 1
			except:
				name = dirName
				season = -1
				episode = -1
		else: # Movie
			season = -1
			episode = -1
			res = re.search("(.*)\.[0-9]{4}\.", dirName.lower())
			if not res:
				res = re.search("(.*)\.(1080p|720p)\.", dirName.lower())
			if res:
				res = res.groups()
				name = ""
				for s in res[0].split("."):
					if len(s) > 1:
						name = name + s[0].upper() + s[1:] + " "
					elif len(s) == 1:
						name = name + s[0].upper() + " "
				name = name[:-1]
			else:
				name = dirName
				failbit = 1
		
		return (name, season, episode, failbit)
