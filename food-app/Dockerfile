FROM node:24

WORKDIR /food-app

COPY package*.json ./

RUN npm ci --omit=dev

COPY . .

EXPOSE 3002

CMD ["npm", "start"]