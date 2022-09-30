#/bin/bash
CMD="docker-compose exec api bash"
echo $CMD
$CMD


# python manage.py migrate

# python manage.py makemigrations polls
# python manage.py sqlmigrate polls 0001
# python manage.py check
# python manage.py migrate

# python manage.py createsuperuser
# U: admin
# E: admin@mail.com
# P: django
