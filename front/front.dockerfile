FROM node:16.15.0
USER root

WORKDIR /front
COPY ./package*.json /front
ENV PATH="/front/node_modules/.bin:${PATH}"
RUN npm install

COPY . /front
