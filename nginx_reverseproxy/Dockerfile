FROM nginx:alpine
RUN apk add bash
COPY default.conf /etc/nginx/conf.d/
#COPY flask.conf /etc/nginx/site-available/
#RUN mkdir /etc/nginx/site-enabled && ln -s /etc/nginx/site-available/flask.conf /etc/nginx/site-enabled/flask.conf
#EXPOSE 80
ENTRYPOINT ["nginx","-g","daemon off;"]
#CMD ["bash"]

