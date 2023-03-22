FROM node:lts-alpine as build-stage
WORKDIR /app
COPY ./services/front/package*.json ./
RUN npm install
COPY ./services/front ./
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./services/front/nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]