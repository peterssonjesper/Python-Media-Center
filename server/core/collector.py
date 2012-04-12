#!/usr/bin/python

import httplib, sys, json, os, inspect, time
run_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])
sys.path.insert(0, run_folder + "/core")

from db import *
from threading import Thread
from urllib import urlretrieve

class Collector(Thread):
  def __init__(self):
    Thread.__init__(self)
  def run(self):
    self.db = Db()
    while True:
      movies = self.db.get_movies(True)
      if len(movies) == 0:
        time.sleep(60)
      else:
        self.collect_movies(movies);
    self.db.disconnect()

  def collect_movies(self, movies):
    conn = httplib.HTTPConnection("api.rottentomatoes.com")
    for entry in movies:
      title = entry['title']
      search_string = title.replace(" ", "%20");
      print "Collecting data from IMDB: " + title
      conn.request("GET", "/api/public/v1.0/movies.json?apikey=p562cyb8c6f2kcn5a5xqzsdn&q=" + search_string)
      r = conn.getresponse()
      json_data = r.read()
      movieData = {}
      movieData['scraped'] = 1
      try:
        data = json.loads(json_data)
        if data['total'] > 0:
          movie = data['movies'][0]
          movieData['title'] = movie['title']
          movieData['rating'] = movie['ratings']['audience_score']
          movieData['year'] = movie['year']
          movieData['released'] = movie['release_dates']['dvd']
          movieData['overview'] = movie['synopsis']
          movieData['runtime'] = movie['runtime']
          movieData['imdb_id'] = movie['alternate_ids']['imdb']
          self.db.update_movies(entry['id'], movieData);
          urlretrieve(movie['posters']['original'], "server/db/posters/movies/" + str(entry['id']) + "_original.jpg")
          urlretrieve(movie['posters']['detailed'], "server/db/posters/movies/" + str(entry['id']) + "_detailed.jpg")
          urlretrieve(movie['posters']['profile'], "server/db/posters/movies/" + str(entry['id']) + "_profile.jpg")
          urlretrieve(movie['posters']['thumbnail'], "server/db/posters/movies/" + str(entry['id']) + "_thumbnail.jpg")
        else:
          self.db.update_movies(entry['id'], {"scraped" : 1});
      except:
        print "Could not parse answer for " + title
      self.db.commit()
      time.sleep(10)
