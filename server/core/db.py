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
 
  # Creates a new clean db
  def create_db(self):
    self.cursor.execute('''create table files ( id integer primary key autoincrement, name text, filename text, inner_dir text, base_dir text, media_id integer, media_type integer, video_quality text, audio_quality text, failbit integer)''')
    self.cursor.execute('''create table series ( id integer primary key autoincrement, name text, title text, imdb_id text, rating real, num_ratings integer, actors text, aired text, genre text, overview text, tvdb_id text, scraped integer )''')
    self.cursor.execute('''create table episodes ( id integer primary key autoincrement, title text, season integer, episode integer, series_id integer, tvdb_id text, imdb_id text, rating real, num_ratings integer, guest_actors text, aired text, overview text, director text, writer text, watched integer, scraped integer )''')
    self.cursor.execute('''create table movies ( id integer primary key autoincrement, name text, title text, imdb_id text, rating real, year integer, released text, genre text, director text, writer text, actors text, overview text, runtime text, watched integer, scraped integer)''')

  # Insert a new media to DB
  def insert_media(self, data):
    media_type = data['media_type']
    name = data['name']

    # Look in data if the title can be found, if so set media_id
    table = "series" if media_type == 1 else "movies"
    self.cursor.execute("select count(id), id from " + table + " where name = ? limit 1", [name])
    row = self.cursor.fetchone()
    media_id = -1
    if row[0] > 0 and data['failbit'] == 0: # Name already in DB
      media_id = row[1]
      if media_type == 1: # Series in DB, insert episode if it does not exist
        self.cursor.execute("select count(id), id from episodes where series_id = ? and episode = ? and season = ? limit 1", [media_id, data['episode'], data['season']])
        row = self.cursor.fetchone()
        if row[0] == 0: # Episode does not exist
          data['series_id'] = media_id
          media_id = self.insert_episode(data)
        else:
          media_id = row[1]
    elif data['failbit'] == 0: # Name not in DB
      if media_type == 1:
        series_id = self.insert_series(data) # Create series
        data['series_id'] = series_id
        media_id = self.insert_episode(data) # Insert episode
      else:
        media_id = self.insert_movie(data) # Insert movie

    data['media_id'] = media_id
    self.insert_file(data)
  
  # Disconnects from DB
  def disconnect(self):
    self.cursor.close()
  
  # Inserts a file into the files table
  def insert_file(self, data):
    name = data['name'] if "name" in data.keys() else "UNKNOWN"
    filename = data['filename'] if "filename" in data.keys() else ""
    inner_dir = data['inner_dir'] if "inner_dir" in data.keys() else ""
    base_dir = data['base_dir'] if "base_dir" in data.keys() else ""
    media_id = data['media_id'] if "media_id" in data.keys() else -1
    media_type = data['media_type'] if "media_type" in data.keys() else 0
    video_quality = data['video_quality'] if "video_quality" in data.keys() else ""
    audio_quality = data['audio_quality'] if "audio_quality" in data.keys() else ""
    failbit = data['failbit'] if "failbit" in data.keys() else 0
    self.cursor.execute("insert into files values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [name, filename, inner_dir, base_dir, media_id, media_type, video_quality, audio_quality, failbit])
    id = self.cursor.lastrowid
    return id

  # Inserts an episode into the episode table
  def insert_episode(self, data):
    title = data['title'] if "title" in data.keys() else ""
    season = data['season'] if "season" in data.keys() else 0
    episode = data['episode'] if "episode" in data.keys() else 0
    series_id = data['series_id'] if "series_id" in data.keys() else -1
    tvdb_id = data['tvdb_id'] if "tvdb_id" in data.keys() else ""
    imdb_id = data['imdb_id'] if "imdb_id" in data.keys() else ""
    rating = data['rating'] if "rating" in data.keys() else 0
    num_ratings = data['num_ratings'] if "num_ratings" in data.keys() else 0
    guest_actors = data['guest_actors'] if "guest_actors" in data.keys() else ""
    aired = data['aired'] if "aired" in data.keys() else ""
    overview = data['overview'] if "overview" in data.keys() else ""
    director = data['director'] if "director" in data.keys() else ""
    writer = data['writer'] if "writer" in data.keys() else ""
    watched = 0
    scraped = 0
    self.cursor.execute("insert into episodes values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [title, season, episode, series_id, tvdb_id, imdb_id, rating, num_ratings, guest_actors, aired, overview, director, writer, watched, scraped])
    media_id = self.cursor.lastrowid
    return media_id

  # Inserts a series into the series table
  def insert_series(self, data):
    name = data['name'] if "name" in data.keys() else ""
    title = data['title'] if "title" in data.keys() else ""
    imdb_id = data['imdb_id'] if "imdb_id" in data.keys() else ""
    tvdb_id = data['tvdb_id'] if "tvdb_id" in data.keys() else ""
    rating = data['rating'] if "rating" in data.keys() else 0
    num_ratings = data['num_ratings'] if "num_ratings" in data.keys() else 0
    actors = data['actors'] if "actors" in data.keys() else ""
    aired = data['aired'] if "aired" in data.keys() else ""
    genre = data['genre'] if "genre" in data.keys() else ""
    overview = data['overview'] if "overview" in data.keys() else ""
    scraped = 0
    self.cursor.execute("insert into series values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [name, title, imdb_id, rating, num_ratings, actors, aired, genre, overview, tvdb_id, scraped])
    series_id = self.cursor.lastrowid
    return series_id

  # Inserts a movie into the movie table
  def insert_movie(self, data):
    name = data['name'] if "name" in data.keys() else ""
    title = data['title'] if "title" in data.keys() else ""
    imdb_id = data['imdb_id'] if "imdb_id" in data.keys() else ""
    rating = data['rating'] if "rating" in data.keys() else 0
    year = data['year'] if "year" in data.keys() else 0
    released = data['released'] if "released" in data.keys() else ""
    genre = data['genre'] if "genre" in data.keys() else ""
    director = data['director'] if "director" in data.keys() else ""
    writer = data['writer'] if "writer" in data.keys() else ""
    actors = data['actors'] if "actors" in data.keys() else ""
    overview = data['overview'] if "overview" in data.keys() else ""
    runtime = data['runtime'] if "runtime" in data.keys() else ""
    watched = 0
    scraped = 0
    self.cursor.execute("insert into movies values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [name, title, imdb_id, rating, year, released, genre, director, writer, actors, overview, runtime, watched, scraped])
    media_id = self.cursor.lastrowid
    return media_id

  # Returns a list of all series
  def get_series(self):
    q = ""
    q += "select distinct series.id, series.name, series.title from files "
    q += "join episodes on files.media_id = episodes.id "
    q += "join series on series.id = episodes.series_id where files.media_type=1 and files.failbit=0 order by series.title, series.name"
    self.cursor.execute(q)
    res = []
    for row in self.cursor:
      title = row[2] if row[2] else row[1]
      res.append({"id" : row[0], "title" : title})
    return res

  # Returns a list of all seasons for given series
  def get_seasons(self, series_id):
    q = ""
    q += "select distinct episodes.season from files "
    q += "left outer join episodes on files.media_id = episodes.id "
    q += "where files.media_type = 1 and episodes.series_id = ? and files.failbit = 0"
    self.cursor.execute(q, [series_id])
    res = []
    for row in self.cursor:
      res.append(row[0])
    return res

  # Returns all episodes for given series and season
  def get_episodes(self, series_id, season):
    q = ""
    fields = "episodes.id, name, filename, inner_dir, base_dir, video_quality, audio_quality, title, episode, rating, num_ratings, guest_actors, aired, overview, director, writer, watched"
    q += "select distinct " + fields + " from files "
    q += "join episodes on files.media_id = episodes.id "
    q += "where files.media_type=1 and episodes.season=? and episodes.series_id=? and files.failbit=0"
    self.cursor.execute(q, [season, series_id])
    res = []
    for row in self.cursor:
      title = row[7] if row[7] else row[1]
      res.append({
        "id" : row[0],
        "title" : title,
        "filename" : row[2],
        "inner_dir" : row[3],
        "base_dir" : row[4],
        "video_quality" : row[5],
        "audio_quality" : row[6],
        "episode" : row[8],
        "rating" : row[9],
        "guest_actors" : row[10],
        "aired" : row[11],
        "overview" : row[12],
        "director" : row[13],
        "writer" : row[14],
        "watched" : row[15]
      });
    return res

  # Returns a list of alla movies
  def get_movies(self, only_non_scraped = False):
    fields = "movies.id, files.name, filename, inner_dir, base_dir, video_quality, audio_quality, title, rating, year, released, genre, director, writer, actors, overview, runtime, watched"
    q = ""
    q += "select " + fields + " from files "
    q += "join movies on files.media_id = movies.id "
    q += "where files.media_type=2 and files.failbit=0 "
    if only_non_scraped:
      q += "and movies.scraped = 0"
    self.cursor.execute(q)
    res = []
    for row in self.cursor:
      title = row[7] if row[7] else row[1]
      res.append({
        "id" : row[0],
        "title" : title,
        "filename" : row[2],
        "inner_dir" : row[3],
        "base_dir" : row[4],
        "video_quality" : row[5],
        "audio_quality" : row[6],
        "rating" : row[8],
        "year" : row[9],
        "released" : row[10],
        "genre" : row[11],
        "director" : row[12],
        "writer" : row[13],
        "actors" : row[14],
        "overview" : row[15],
        "runtime" : row[16],
        "watched" : row[17]
      });
    return res

  def update_movies(self, id, data):
    q = "update movies set "
    for attr in data.keys():
      q += attr + "=?,"
    q = q[:-1] if len(data.keys()) > 0 else q
    q += " where id=?"
    vals = []
    for attr in data.keys():
      vals += [data[attr]]
    vals += [id]
    self.cursor.execute(q, vals)
