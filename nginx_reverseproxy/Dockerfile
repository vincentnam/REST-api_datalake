FROM nginx:alpine
RUN apk add bash
COPY default.conf /etc/nginx/conf.d/
#EXPOSE 80
ENTRYPOINT ["nginx","-g","daemon off;"]
#CMD ["bash"]

