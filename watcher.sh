#!/bin/bash

set -e

while true
do
	echo "starting watcher..."
    python manage.py watchgroups
	sleep 1
done
