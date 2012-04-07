from listview import *
from msg import *
from file import *

class Navigation:
	def __init__(self, listview, player, api, window):
		self.listView = listview;
		self.player = player;
		self.window = window
		self.msg = Msg(self.window);
		self.listView.onAction(self.onListViewAction)
		self.api = api

	def showRoot(self, takeFocus = True):
		self.listView.setTitle("Welcome!");
		self.currentView = "root"
		mainMenu = [ListItem("Movies"), ListItem("TV")]
		mainMenu[0].setAttr("category", "movies")
		mainMenu[1].setAttr("category", "tv")
		self.listView.setListItems(mainMenu);
		if takeFocus:
			self.window.setFocus("listview")
	
	def showSeries(self):
		self.listView.setTitle("TV Series");
		self.currentView = "tv"
		listItems = []
		for i in self.api.getSeries():
			l = ListItem(i['title'])
			l.setAttr("media_id", i['media_id'])
			l.setAttr("title", i['title'])
			listItems.append(l)
		self.listView.setListItems(listItems);
		self.window.setFocus("listview")

	def showMovies(self):
		self.listView.setTitle("Movies");
		self.currentView = "movies"
		listItems = []
		for i in self.api.getMovies():
			l = ListItem(i['title'])
			l.setAttr("file", File(i['base_dir'], i['inner_dir'], i['filename']))
			l.setAttr("media_id", i['media_id'])
			l.setAttr("title", i['title'])
			listItems.append(l)
		self.listView.setListItems(listItems);
		self.window.setFocus("listview")

	def showSeasons(self, media_id, title):
		self.listView.setTitle("TV Series / " + title);
		self.currentView = "seasons"
		listItems = []
		for i in self.api.getSeasons(media_id):
			l = ListItem("Season " + str(i))
			l.setAttr("season", i)
			l.setAttr("media_id", media_id)
			listItems.append(l)
		self.listView.setListItems(listItems);
		self.window.setFocus("listview")

	def showEpisodes(self, media_id, season):
		self.currentView = "episodes"
		listItems = []
		for i in self.api.getEpisodes(media_id, season):
			l = ListItem("Episode " + str(i["episode"]))
			l.setAttr("media_id", i['media_id'])
			l.setAttr("title", i['title'])
			l.setAttr("season", i["season"])
			l.setAttr("episode", i["episode"])
			l.setAttr("file", File(i['base_dir'], i['inner_dir'], i['filename']))
			listItems.append(l)
			title = i['title']
		self.listView.setTitle("TV Series / " + title + " / Season " + str(season));
		self.listView.setListItems(listItems);
		self.window.setFocus("listview")
	
	def onListViewAction(self, action, item):
		if action == "enter":
			self.onSelection(item)
		elif action == "esc":
			self.onEscape(item)
		elif action == "f5":
			self.api.resync()
			self.msg.viewMsg("Sync complete!")
			self.showRoot(False)

	def onSelection(self, item):
		if self.currentView == "root":
			if item.getAttr("category") == "tv": # List TV
				self.showSeries()
			else: # List movies
				self.showMovies()

		elif self.currentView == "tv":
			self.showSeasons(item.getAttr("media_id"), item.getAttr("title"))

		elif self.currentView == "seasons":
			self.showEpisodes(item.getAttr("media_id"), item.getAttr("season"))

		elif self.currentView == "episodes":
			s = str(item.getAttr("season"))
			if len(s) == 1:
				s = "0" + s
			e = str(item.getAttr("episode"))
			if len(e) == 1:
				e = "0" + e
			self.msg.viewMsg("Will now play\n\n" + item.getAttr("title") + " S" + s + "E" + e)
			self.player.play_file(item.getAttr("file").get_path())

		elif self.currentView == "movies":
			self.msg.viewMsg("Will now play\n\n" + item.getAttr("title"))
			self.player.play_file(item.getAttr("file").get_path())

	def onEscape(self, listItem):
		if self.currentView == "tv" or self.currentView == "movies":
			self.showRoot()
		elif self.currentView == "seasons":
			self.showSeries()
		elif self.currentView == "episodes":
			self.showSeasons(listItem.getAttr("media_id"), listItem.getAttr("title"))
