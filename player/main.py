#! /usr/bin/python
import config, os, inspect, sys
run_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])
sys.path.insert(0, run_folder + "/gui")
sys.path.insert(0, run_folder + "/core")

from player import *
from listview import *
from window import *
from navigation import *
from api import *

class App:
	def __init__(self):
		self.window = Window()
		self.player = Player();
		self.listView = ListView(self.window)
		self.api = Api()
		self.navigation = Navigation(self.listView, self.player, self.api, self.window)

		self.navigation.showRoot()

		self.window.render()

if __name__ == "__main__":
	App();
