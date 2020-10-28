FROM python:latest

RUN apt-get update -y
# We copy just the requirements.txt first to leverage Dockerv cache
COPY ./requirements.txt /app/requirements.txt
#WORKDIR /app
RUN mkdir /flask_tmp
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
COPY ["app.py" , "/app/"]

ENTRYPOINT [ "python" ]

CMD [ "/app/app.py" ]
#RUN apt-get install -y nginx
#COPY supervisord/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
#CMD ["bash"]
#CMD ["/usr/bin/supervisord"]
