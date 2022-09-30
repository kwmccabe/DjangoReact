#/bin/bash

CMD="docker-compose exec db psql --username=postgres_user --dbname=django_react"
echo $CMD
$CMD


# PSQL CMD
# \h {cmd} - help {for command}
# \l - show databases
# \c dbname - connect to database
# \d - show all
# \dt - show tables
# \q - quit
