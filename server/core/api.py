import socket
import json
import config
import sys
import os

class Api:
	def __init__(self, db, sync):
		self.db = db
		self.sync = sync
		try:
			self.s = socket.socket()
			self.s.bind((config.ip, config.port))
			self.s.listen(5)
		except:
			print "Could not start socket... Permissions?"
			sys.exit(0)

	def start(self):
		while True:
			c, addr = self.s.accept()
			json_data = c.recv(1024)
			try:
				data = json.loads(json_data)
				print "Received command " + data['cmd']

				if data['cmd'] == "getseries":
					q = "select distinct media.id, media.title, metadata.title as metadata_title from media join files on files.media_id = media.id left outer join metadata on metadata.id = media.metadata_id where media_type=1 and failbit=0 order by media.title"
					self.db.getCursor().execute(q)
					res = []
					for row in self.db.getCursor():
						title = row[2] if row[2] else row[1]
						res.append({"media_id" : row[0], "title" : title})
					c.send(json.dumps(res))

				if data['cmd'] == "getseasons":
					media_id = data["media_id"]
					q = "select distinct season from files where media_id= ? and media_type = 1"
					self.db.getCursor().execute(q, [media_id])
					res = []
					for row in self.db.getCursor():
						res.append(row[0])
					c.send(json.dumps(res))

				if data['cmd'] == "getepisodes":
					media_id = data["media_id"]
					season = data["season"]
					q = "select filename, inner_dir, base_dir, season, episode, media.title, metadata.title, media_id from files join media on media.id = files.media_id left outer join metadata on metadata.id = media.metadata_id where media_id=? and season=? and media_type = 1 order by season, episode, media.title"
					self.db.getCursor().execute(q, [media_id, season])
					res = []
					for row in self.db.getCursor():
						title = row[6] if row[6] else row[5]
						res.append({"filename" : row[0], "inner_dir" : row[1], "base_dir" : row[2], "season" : row[3], "episode" : row[4], "title" : title, "media_id" : row[7]})
					c.send(json.dumps(res))

				if data['cmd'] == "getmetadata":
					media_id = data["media_id"]
					q = "select metadata_id from media where id=?"
					self.db.getCursor().execute(q, [media_id])
					row = self.db.getCursor().fetchone()

					q = "select rating, year, released, genre, director, writer, actors, plot, poster, runtime from metadata where id=?"
					self.db.getCursor().execute(q, [row[0]])
					row = self.db.getCursor().fetchone()
					rating = row[0] if row else ""
					year = row[1] if row else ""
					released = row[2] if row else ""
					genre = row[3] if row else ""
					director = row[4] if row else ""
					writer = row[5] if row else ""
					actors = row[6] if row else ""
					plot = row[7] if row else ""
					poster = row[8] if row else ""
					runtime = row[9] if row else ""
					ans = {"rating" : rating, "year" : year, "released" : released, "genre" : genre, "director" : director, "writer" : writer, "actors" : actors, "plot" : plot, "poster" : poster, "runtime" : runtime}
					c.send(json.dumps(ans))

				if data['cmd'] == "getposter":
					media_id = data['media_id']
					path = "posters/" + str(media_id) + ".jpg" if os.path.exists("posters/" + str(media_id) + ".jpg") else "posters/unknown.jpg"
					f = open(path, "r")
					c.send(f.read())
					f.close()

				if data['cmd'] == "getmovies":
					q = "select filename, inner_dir, base_dir, media_id, media.title, metadata.title from files join media on media.id = files.media_id left outer join metadata on metadata.id = media.metadata_id where media_type = 2 order by media.title"
					self.db.getCursor().execute(q)
					res = []
					for row in self.db.getCursor():
						title = row[5] if row[5] else row[4]
						res.append({"filename" : row[0], "inner_dir" : row[1], "base_dir" : row[2], "title" : title, "media_id" : row[3]})
					c.send(json.dumps(res))

				elif data['cmd'] == "shutdown":
					ans = {"msg" : "bye"}
					c.send(json.dumps(ans))
					c.close()
					break

				elif data['cmd'] == "resync":
					self.sync.initSync()
					ans = {"msg" : "ok"}
					c.send(json.dumps(ans))

			except:
				print "Could not understand the request " + json_data
				pass
			c.close()
