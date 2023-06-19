FROM node:16.15.0

COPY . /front

WORKDIR /front
ENV PATH="/front/node_modules/.bin:${PATH}"
RUN npm install
