import sqlite3, os

class Db:
	def __init__(self):
		create_db = not os.path.exists("server/db/db.sqlite") or os.path.getsize("server/db/db.sqlite") == 0
		self.conn = sqlite3.connect('server/db/db.sqlite')
		self.cursor = self.conn.cursor()
		if create_db:
			print "Could not locate DB, will create a new one"
			self.create_db()
		self.conn.text_factory = str
	
	# Removes all entries in DB
	def erase(self):
		self.cursor.execute('''delete from files''');

	def commit(self):
		self.conn.commit()
	
	def getCursor(self):
		return self.cursor
	
	# Creates a new clean db
	def create_db(self):
		self.cursor.execute('''create table files ( id integer primary key autoincrement, filename text, inner_dir text, base_dir text, media_id integer, media_type integer, quality text, failbit integer)''')
		self.cursor.execute('''create table series ( id integer primary key autoincrement, name text, title text, imdb_id text, rating real, num_ratings integer, actors text, aired text, genre text, overview text, series_id integer, fetched integer )''')
		self.cursor.execute('''create table episodes ( id integer primary key autoincrement, title text, season integer, episode integer, series_id integer, episode_id integer, imdb_id text, rating real, num_ratings integer, guest_actors text, aired text, overview text, director text, writer text, watched integer )''')
		self.cursor.execute('''create table movies ( id integer primary key autoincrement, name text, title text, imdb_id text, rating text, year text, released text, genre text, director text, writer text, actors text, overview text, runtime text, watched integer)''')
	
	# Insert a new media to DB
	def insert_file(self, data):
		title = data["title"] if "title" in data.keys() else "UNKNOWN"

		# Look in data if the title can be found, if so set media_id
		imdb_id = ""
		self.cursor.execute("select id from media where title = ?", [title])
		row = self.cursor.fetchone()
		if row:
			media_id = row[0]
		else:
			self.cursor.execute("insert into media values (null, ?, '')", [title])
			media_id = self.cursor.lastrowid
			row = self.cursor.fetchone()

		filename = data["filename"]
		base_dir = data["base_dir"]
		inner_dir = data["inner_dir"]
		season = data["season"]
		episode = data["episode"]
		media_type = data["media_type"]
		failbit = data["failbit"]
		self.cursor.execute('insert into files values(null, ?, ?, ?, ?, ?, ?, ?, ?)', (filename, inner_dir, base_dir, season, episode, media_id, media_type, failbit));

	def getEntryWithoutMetadata(self):
		self.cursor.execute("select id, title from media where metadata_id = '' order by title limit 1")
		row = self.cursor.fetchone()
		return row

	def insertMetadata(self, media_id, data):
		self.cursor.execute("insert into metadata values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
			data['ID'], data['Title'], data['Rating'], data['Year'], data['Released'], data['Genre'],
			data['Director'], data['Writer'], data['Actors'], data['Plot'], data['Poster'], data['Runtime']
		])
		self.updateMetadataId(media_id, self.cursor.lastrowid)
	
	def updateMetadataId(self, media_id, metadata_id):
		self.cursor.execute("update media set metadata_id = ? where id = ?", [metadata_id, media_id])
	
	def disconnect(self):
		self.cursor.close()
