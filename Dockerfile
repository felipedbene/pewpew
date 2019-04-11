# this same shows how we can extend/change an existing official image from Docker Hub

FROM nginx:latest
# highly recommend you always pin versions for anything beyond dev/learn
    
WORKDIR /usr/share/nginx/html

COPY ./docs/ .
COPY nginx.conf /etc/nginx/conf.d/default.conf
