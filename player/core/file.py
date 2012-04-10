import config, socket

class File:
	def __init__(self, base_dir, inner_dir, filename):
		self.filename = filename
		self.base_dir = base_dir
		self.inner_dir = inner_dir

	def get_path(self):
		if config.mode == "master":
			return self.base_dir + "/" + self.inner_dir + "/" + self.filename
		else:
			try:
				return config.mapped_directories[self.base_dir] + "/" + self.inner_dir + "/" + self.filename
			except:
				print "Error! The directory " + str(self.base_dir) + " is not mapped!"
				return False
