#!/bin/bash
# PATH_TO_FLASK=/datalake/frontend/
PATH_TO_FLASK=/data/python-project/
sudo docker build -t rest_api .
sudo docker run -p 5000:5000 -v REST-api_datalake/:/app/ -v /datalake/flask_tmp/:/flask_tmp rest_api
