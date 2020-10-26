#!/bin/bash
PATH_REACT_FOLDER=${pwd}
sudo docker build -t rest_api .
echo $PATH_REACT_FOLDER
sudo docker run -it -p 5000:5000 -v ${PATH_TO_FLASK}:/app/ -v /datalake/flask_tmp/:/flask_tmp rest_api
