import os, sys
working_folder = os.path.abspath(os.path.dirname(sys.argv[0]))

### What mode to use
# master: Runs database and player
# server: Runs database only
# slave: Runs player only, conncets to remote database
mode = "master"

### If an initial sync should be performed when starting
# Applies to modes: Master, server
initsync = True

### Which IP address and port to start on
# Applies to modes: Master, server
ip = "127.0.0.1"
port = 31337

### The following directories will be indexed
# Applies to modes: Master, server
watchDirs = [
	#"/path/on/disk"
]

### What media player that will be used
# Applies to modes: Master, slave
player_path = working_folder + "/player/core/playrar.sh"

### What endings that are accepted to be indexed as playable
# Applies to modes: Master, slave
acceptedEndings = ["mkv", "avi", "iso", "img", "rar"]

### IP address and port that the server runs on
# Applies to modes: Slave
server_ip = "192.168.0.1"
server_port = 31337;

### Maps local directories to server
# Applies to modes: Slave
mapped_directories = {
	#"/path/on/server" : "/path/on/slave"
}
