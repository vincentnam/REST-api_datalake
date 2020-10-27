FROM python:latest

RUN apt-get update -y && apt-get install -y supervisor

# We copy just the requirements.txt first to leverage Dockerv cache
RUN mkdir /flask_tmp && mkdir /app
COPY ./requirements.txt /app/requirements.txt
#WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
COPY ["app.py" , "templates/", "/app/"]

#ENTRYPOINT [ "python" ]

#CMD [ "/app.py" ]
RUN apt-get install -y nginx
COPY supervisord/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["bash"]
#CMD ["/usr/bin/supervisord"]
