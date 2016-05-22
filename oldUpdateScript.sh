#!/bin/bash
# TODO: Pull list of all repositories from https://api.github.com/orgs/OpenAgInitiative/repos and compare to what you have checked out (to see if anything new pops up ;) )

directories=$(ls -d */)

for directory in $directories; do
	echo -e "Updating $(tput bold)\033[37;1m$directory\033[0m"
	cd $directory && git up | sed 's/^/      /'
	cd ..
done
