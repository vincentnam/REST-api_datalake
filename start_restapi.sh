#!/bin/bash
PATH_REACT_FOLDER=${pwd}
git pull
sudo docker build -t rest_api .
sudo docker run -it -p 5000:5000 -v ${PATH_TO_FLASK}/:/app/ -v /datalake/flask_tmp/:/flask_tmp rest_api
