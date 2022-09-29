FROM node

RUN mkdir /app
WORKDIR /app

ADD package.json ./
ADD package-lock.json ./
RUN npm install

ADD . .
