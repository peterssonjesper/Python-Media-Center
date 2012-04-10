#! /usr/bin/python
import config, os, sys
from threading import Thread

working_folder = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.insert(0, working_folder + "/player/gui")
sys.path.insert(0, working_folder + "/player/core")

from mediaplayer import *
from listview import *
from window import *
from navigation import *
from apiclient import *

class Player():
	def run(self):
		self.window = Window()
		self.mediaplayer = Mediaplayer();
		self.listView = ListView(self.window)
		self.api = Apiclient()
		self.navigation = Navigation(self.listView, self.mediaplayer, self.api, self.window)

		self.navigation.showRoot()
		self.listView.printListItems();

		self.window.render()
