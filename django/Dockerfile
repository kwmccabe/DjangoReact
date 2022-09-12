FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ADD . .


### SAMPLE ###
# FROM python:3.4
#
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         postgresql-client \
#     && rm -rf /var/lib/apt/lists/*
#
# WORKDIR /app/api
# COPY requirements.txt /app/api
# RUN pip install -r requirements.txt
#
# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



### SAMPLE ###
# pull official base image
# FROM python:3.10-alpine

# set work directory
# WORKDIR /app

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
# RUN apk update \
#  && apk add gcc python3-dev

# install python dependencies
# COPY requirements.txt /app/requirements.txt
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt


# copy project
# COPY . .
