#!/usr/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./export_data.sh <dbname> <output dir>"
	exit;
fi

if [ -d "$2" ]; then
	rm -r "$2"
fi

mkdir "$2"
psql -d $1 -f 