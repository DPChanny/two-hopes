FROM node:slim

WORKDIR /web

COPY package*.json ./
RUN npm install

COPY ./ ./

EXPOSE ${WEB_PORT}

CMD ["npm", "start"]
