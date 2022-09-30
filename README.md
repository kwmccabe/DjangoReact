# DjangoReact

This project is based on the official [Django Tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/ "Writing your first Django app, part 1").  But, there are several enhancements:

### Docker-Compose
- The project has been 'dockerized' into three containers : `db`, `api', and `web`.
- `db` runs PostgreSQL on the official [postgres](https://hub.docker.com/_/postgres) image.
- `api` runs Django on the official [python](https://hub.docker.com/_/python) image.
- `web` runs ReactJS on the official [node](https://hub.docker.com/_/node) image.
- Launch containers : `docker-compose up --build`

### PostgreSQL
- Connect : `docker-compose exec db psql --username=postgres_user --dbname=django_react`
- A `postgresql.conf` file is provided for tuning [database parameters](https://www.postgresql.org/docs/current/config-setting.html "20.1. Setting Parameters").

### Django
- Connect : `docker-compose exec api bash`
- Some basic Django commands (to run *after* connecting) are stored in `/app/bin`. (eg, `django-migrate.sh` and `django-createsuperuser.sh`)
- "Polls" have been added to the tutorial's "Questions" and "Choices".
- The Admin sections for each type have been extended to better show the model hierarchy.
- The public pages have been cleaned up with [Bootstrap](https://django-bootstrap-v5.readthedocs.io/ "django-bootstrap-v5").
- API endpoints have been added using [Django REST](https://www.django-rest-framework.org/ "Django REST framework")

### ReactJS
- Connect : `docker-compose exec web bash`
- Look at the `react/README.md` file to get oriented.
- The `package.json` file defines the `proxy` link to the API/Django container.  (see [Create React App](https://create-react-app.dev/docs/proxying-api-requests-in-development/ "Proxying API Requests in Development"))
- [React Router](https://reactrouter.com/ "React Router") was added for client-side routing.
- [React Bootstrap](https://react-bootstrap.github.io/ "React Bootstrap") was added for layout.
