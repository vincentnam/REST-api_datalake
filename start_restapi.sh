#!/bin/bash
sudo docker build -t rest_api .
sudo docker run -p 5000:5000 -v /datalake/frontend/REST-api_datalake/:/app/ -v /datalake/flask_tmp/:/flask_tmp rest_api
