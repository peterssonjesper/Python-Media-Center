import os

# Server IP and port
server_ip = "192.168.0.1"
server_port = 31337;

# Path to the player to use, could be for example the playrar-script or simply just mplayer
player_path = os.getcwd() + "/core/playrar.sh"

# Maps local directories to server
mapped_directories = {
	#"/path/on/server" : "/path/on/player/machine"
}
