#/bin/bash

BASEDIR="/Users/kwmccabe/Documents/WEBDEV/docker-hub/django-react"

CMD="docker-compose -f $BASEDIR/docker-compose.yml up --build"
echo $CMD
$CMD


