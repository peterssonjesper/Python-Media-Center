#!/bin/bash
export DISPLAY=:0.0

MPLAYER_FLAGS="-fs -vo vdpau -quiet"
MPLAYER_FLAGS_HD="-vc ffh264vdpau -demuxer lavf"

FUSERMOUNT="/usr/bin/fusermount"
MOUNT_FUSE="/sbin/mount.fuse"
RARFS="/usr/local/bin/rarfs"
MPLAYER="/usr/bin/mplayer"
MOUNT_DIR="/tmp/rar"

if [ $(uname) = "Darwin" ]; then
	MPLAYER="/Applications/MPlayer OSX Extended.app/Contents/Resources/Binaries/mpextended.mpBinaries/Contents/mpextended-mt.mpBinaries/Contents/MacOS/mplayer"
	MPLAYER_FLAGS="-fs"
	MPLAYER_FLAGS_HD=""
fi

FILE=$1

if [ -a "$FILE" ]; then
	MPLAYER_PID=$(ps x | grep -i mplayer | grep -v grep | awk '{ print $1 }')
	if [ $MPLAYER_PID ]; then
		kill $MPLAYER_PID
		sleep 2 # Wait for unmount
	fi
	FILETYPE=$(file -ib "$FILE" | awk '{print $1}')
	ENDING=$(echo "$FILE"|awk -F . '{print $NF}')
	if [ $FILETYPE = "application/x-rar;" -a $ENDING = "rar" ]; then
		echo "Playing $FILE ..."
		if [ ! -d "$MOUNT_DIR" ]; then
			mkdir $MOUNT_DIR
		fi
		sudo $FUSERMOUNT -u $MOUNT_DIR
		sudo $MOUNT_FUSE $RARFS#$FILE $MOUNT_DIR -o allow_other
		MOUNTED_FILE=$(ls $MOUNT_DIR/*)
		$0 $MOUNTED_FILE
		sudo $FUSERMOUNT -u $MOUNT_DIR
		exit 0
	elif [ $ENDING = "mkv" ]; then
		"$MPLAYER" $MPLAYER_FLAGS $MPLAYER_FLAGS_HD "$FILE"
	elif [ $ENDING = "avi" -o $ENDING = "iso" -o $ENDING = "img" ]; then
		"$MPLAYER" $MPLAYER_FLAGS "$FILE"
	else
		echo "Error: Cannot play file $FILE: Filetype $FILETYPE, with ending $ENDING..."
		exit 2
	fi
else
	echo "Error: File not found!"
	exit 1
fi
