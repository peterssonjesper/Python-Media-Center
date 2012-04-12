#!/usr/bin/python 
import sys, os, getopt
from multiprocessing import Process

working_folder = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.insert(0, working_folder + "/player")
sys.path.insert(0, working_folder + "/server")

from server import *
from player import *
from config import *

if __name__ == "__main__":
	initsync = config.initsync
	mode = config.mode

	if mode == "master" or mode == "server":
		server = Server()
		server.start()

	if mode == "master" or mode == "slave":
		player = Player()
		player.run()
