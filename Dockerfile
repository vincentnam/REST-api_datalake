FROM python:latest

RUN apt-get update -y

# We copy just the requirements.txt first to leverage Dockerv cache
COPY ./requirements.txt /app/requirements.txt
RUN mkdir /flask_tmp
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /.

ENTRYPOINT [ "python" ]

#CMD ["bash"]
CMD [ "app.py" ]

