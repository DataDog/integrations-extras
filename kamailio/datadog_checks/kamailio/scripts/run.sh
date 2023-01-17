#!/bin/sh

if [ $# -eq 0 ]; then
	echo "$0: command to run is required" 1>&2
	exit 1
elif [ "$1" = "kamcmd" ]; then
	# standardize the path then exec
	shift
	sudo -u kamailio /usr/sbin/kamcmd "$@" &&
	exit 0 ||
	exit 1
elif [ "$1" = "getmodules" ]; then
	# find the running proc
	PID=$(pidof kamailio | rev | cut -d ' ' -f 1 | rev)
	if [ ! -e "/proc/$PID/" ]; then
		echo "$0: could not find kamailio process [$PID]" 1>&2
		exit 1
	fi

	# try getting mpath from cmdline args
	while IFS= read -r -d $'\0' ARG; do
		if [ "$ARG" = "-L" ]; then
			IFS= read -r -d $'\0' MPATH
			break
		fi
	done <"/proc/$PID/cmdline"

	# try getting mpath from config
	if [ -z "$MPATH" ] && [ $(kamailio -v | head -1 | grep -oe '[0-9]\.[0-9]\.[0-9]' | cut -d '.' -f -2 | tr -d '.') -gt 54 ]; then
		while IFS= read -r -d $'\0' ARG; do
			if [ "$ARG" = "-f" ]; then
				IFS= read -r -d $'\0' CFG
				break
			fi
		done <"/proc/$PID/cmdline"
	fi

	# otherwise use a sane default
	MPATH=${MPATH:-"kamailio/modules/"}

	# parse out the loaded modules from memory maps
	MAPS=$(sudo -u root /bin/cat /proc/$PID/maps) || {
		echo "$0: could not get memory maps for kamailio process [$PID]" 1>&2
		exit 1
	}
	echo -n "$MAPS" | grep -oe "${MPATH}.*\.so" | sort -u | rev | cut -d '/' -f 1 | cut -d '.' -f 2- | rev
	exit 0
else
	echo "$0: command [$1] is not recognized" 1>&2
	exit 1
fi
