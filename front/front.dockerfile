FROM node:16.15.0
USER root

WORKDIR /front
COPY ./package.json /front/package.json
COPY ./package-lock.json /front/package-lock.json
ENV PATH="/front/node_modules/.bin:${PATH}"
RUN npm install

COPY . /front
