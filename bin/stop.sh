#/bin/bash

BASEDIR="/Users/kwmccabe/Documents/WEBDEV/docker-hub/django-react"

CMD="docker-compose -f $BASEDIR/docker-compose.yml down"
echo $CMD
$CMD

# stop containers ; remove images
#docker rm $(docker ps -a -q)
#docker rmi $(docker images -q)
