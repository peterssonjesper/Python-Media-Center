import socket, json, config, sys, os, time

class Api:
  def __init__(self, db, sync):
    self.db = db
    self.sync = sync
    while True:
      try:
        self.s = socket.socket()
        self.s.bind((config.ip, config.port))
        self.s.listen(5)
        break
      except:
        print "Could not start socket! Will try again in 10 seconds..."
        time.sleep(10)

  def start(self):
    while True:
      c, addr = self.s.accept()
      json_data = c.recv(1024)
      try:
        data = json.loads(json_data)
        print "Received command " + data['cmd']

        if data['cmd'] == "getseries":
          c.send(json.dumps(self.db.get_series()))

        elif data['cmd'] == "getseasons":
          series_id = data["id"]
          c.send(json.dumps(self.db.get_seasons(series_id)))

        elif data['cmd'] == "getepisodes":
          series_id = data["id"]
          season = data["season"]
          c.send(json.dumps(self.db.get_episodes(series_id, season)))

        elif data['cmd'] == "getmovieposter":
          id = data['id']
          try:
            format = data['format']
          except:
            format = "original"
          path = "server/db/posters/movies/" + str(id) + "_" + format + ".jpg" if os.path.exists("server/db/posters/movies/" + str(id) + "_" + format + ".jpg") else "server/db/posters/unknown.jpg"
          f = open(path, "r")
          c.send(f.read())
          f.close()

        elif data['cmd'] == "getepisodeposter":
          id = data['id']
          path = "server/db/posters/episodes/" + str(id) + ".jpg" if os.path.exists("server/db/posters/episodes/" + str(id) + ".jpg") else "server/db/posters/unknown.jpg"
          f = open(path, "r")
          c.send(f.read())
          f.close()

        elif data['cmd'] == "getseriesposter":
          id = data['id']
          path = "server/db/posters/series/" + str(id) + ".jpg" if os.path.exists("server/db/posters/series/" + str(id) + ".jpg") else "server/db/posters/unknown.jpg"
          f = open(path, "r")
          c.send(f.read())
          f.close()

        elif data['cmd'] == "getmovies":
          c.send(json.dumps(self.db.get_movies()))

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
