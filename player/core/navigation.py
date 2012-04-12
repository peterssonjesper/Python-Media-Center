from listview import *
from msg import *
from file import *

class Navigation:
  def __init__(self, listview, mediaplayer, api, window):
    self.listView = listview;
    self.mediaplayer = mediaplayer;
    self.window = window
    self.msg = Msg(self.window);
    self.listView.onAction(self.onListViewAction)
    self.listView.onHover(self.onListViewHover)
    self.api = api

    self.traceStack = [];

  def showRoot(self, takeFocus = True):
    self.listView.setLeftTitle("Welcome!");
    self.currentView = "root"
    mainMenu = [ListItem("Movies"), ListItem("TV")]
    mainMenu[0].setAttr("category", "movies")
    mainMenu[1].setAttr("category", "tv")
    self.listView.setListItems(mainMenu);
    if takeFocus:
      self.window.setFocus("listview")
  
  def showSeries(self):
    self.listView.setLeftTitle("TV Series");
    self.currentView = "tv"
    listItems = []
    for i in self.api.getSeries():
      l = ListItem(i['title'])
      l.setAttr("id", i['id'])
      l.setAttr("title", i['title'])
      listItems.append(l)
    self.listView.setListItems(listItems);
    self.window.setFocus("listview")

  def showMovies(self):
    self.listView.setLeftTitle("Movies");
    self.currentView = "movies"
    listItems = []
    for i in self.api.getMovies():
      l = ListItem(i['title'])
      l.setAttr("file", File(i['base_dir'], i['inner_dir'], i['filename']))
      l.setAttr("id", i['id'])
      l.setAttr("title", i['title'])
      l.setAttr("metadata", i)
      listItems.append(l)
    self.listView.setListItems(listItems);
    self.window.setFocus("listview")

  def showSeasons(self, id, title):
    self.listView.setLeftTitle("TV Series / " + title);
    self.currentView = "seasons"
    listItems = []
    for i in self.api.getSeasons(id):
      l = ListItem("Season " + str(i))
      l.setAttr("season", i)
      l.setAttr("id", id)
      listItems.append(l)
    self.listView.setListItems(listItems);
    self.window.setFocus("listview")

  def showEpisodes(self, id, season):
    self.currentView = "episodes"
    listItems = []
    for i in self.api.getEpisodes(id, season):
      l = ListItem("Episode " + str(i["episode"]))
      l.setAttr("id", i['id'])
      l.setAttr("title", i['title'])
      l.setAttr("season", i["season"])
      l.setAttr("episode", i["episode"])
      l.setAttr("file", File(i['base_dir'], i['inner_dir'], i['filename']))
      listItems.append(l)
      title = i['title']
    self.listView.setLeftTitle("TV Series / " + title + " / Season " + str(season));
    self.listView.setListItems(listItems);
    self.window.setFocus("listview")
  
  def onListViewAction(self, action, item):
    if action == "enter":
      self.onSelection(item)
    elif action == "esc":
      self.onEscape(item)
    elif action == "f5":
      self.msg.viewMsg("Syncing...")
      self.api.resync()
      self.msg.viewMsg("Sync complete!")
      self.showRoot(False)
      self.listView.printListItems();

  def onListViewHover(self, item):
    if self.currentView == "root":
      self.listView.setRightTitle("")
      self.listView.unsetDetailedInfo();
    elif self.currentView == "movies" or self.currentView == "tv":
      metadata = item.getAttr("metadata")
      s = ""
      try:
        if metadata['plot']:
          s += metadata['plot'] + "\n\n"
        if metadata['rating']:
          s += metadata['rating'] + " / 10.0\n"
        if metadata['runtime']:
          s += metadata['runtime'] + "\n"
        if metadata['runtime'] or metadata['rating']:
          s += "\n"
        if metadata['released']:
          s += "Released " + metadata['released'] + "\n"
        if metadata['genre']:
          s += "Genre: " + metadata['genre'] + "\n"
        if metadata['director']:
          s += "Director: " + metadata['director'] + "\n"
        if metadata['writer']:
          s += "Writer: " + metadata['writer'] + "\n"
        if metadata['actors']:
          s += "Actors: " + metadata['actors'] + "\n"
      except:
        pass
      self.listView.setRightTitle(item.getAttr("title"));
      if self.currentView == "movies":
        self.listView.setDetailedInfo(s, self.api.getMoviePoster(item.getAttr("id")))
      else:
        self.listView.setRightTitle("")

  def onSelection(self, item):
    if self.currentView == "root":
      self.traceStack += [self.listView.getSelectedIndex()]
      if item.getAttr("category") == "tv": # List TV
        self.showSeries()
      else: # List movies
        self.showMovies()
      self.listView.printListItems();

    elif self.currentView == "tv":
      self.traceStack += [self.listView.getSelectedIndex()]
      self.showSeasons(item.getAttr("id"), item.getAttr("title"))
      self.listView.printListItems();

    elif self.currentView == "seasons":
      self.traceStack += [self.listView.getSelectedIndex()]
      self.showEpisodes(item.getAttr("id"), item.getAttr("season"))
      self.listView.printListItems();

    elif self.currentView == "episodes":
      self.msg.viewMsg("Loading episode, please wait...")
      self.mediaplayer.play_file(item.getAttr("file").get_path())
      self.mediaplayer.onStarted(self.msg.hideMsg);

    elif self.currentView == "movies":
      self.msg.viewMsg("Loading movie, please wait...")
      self.mediaplayer.play_file(item.getAttr("file").get_path())
      self.mediaplayer.onStarted(self.msg.hideMsg);

  def onEscape(self, listItem):
    if self.currentView == "tv" or self.currentView == "movies":
      self.showRoot()
    elif self.currentView == "seasons":
      self.showSeries()
    elif self.currentView == "episodes":
      self.showSeasons(listItem.getAttr("id"), listItem.getAttr("title"))
    if len(self.traceStack) > 0:
      self.listView.setSelectedIndex(self.traceStack[-1])
      self.traceStack = self.traceStack[:-1]
    self.listView.printListItems();
