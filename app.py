from flask import Flask, request, jsonify, make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import swiftclient.service
from swiftclient.service import SwiftService
import datetime
app = Flask(__name__)
CORS(app,support_credentials = True)
from influxdb_client import InfluxDBClient


def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def get_id(mongodb_url):
    mongo_forid_co = MongoClient(mongodb_url)
    return mongo_forid_co.stats.swift.find_one_and_update({"type": "object_id_file"},   {"$inc": {"object_id": 1}})[
        "object_id"]


def insert_datalake(file_content, user, key, authurl, container_name,
                    file_name=None, application=None, content_type=None,
                    mongodb_url="127.0.0.1:27017", other_data = None ):
    '''
    Insert data in the datalake :
        - In Openstack Swift for data
        - In MongoDB for metadata
    :param file_content: the data to insert :
        with open(file_name, "rb") as f:
            file_data = f.read()
    :type file_content : bytes
    :param user: user for Swift authentication
    :type user : str
    :param key: password for Swift authentication
    :type key : str
    :param authurl: URL for Swift authentication service, commonly :
        http://IP_ADDR:8080/auth/v1.0
    The IP_ADDR is the IP addresse where the service is installed
    (Openstack swift / Openstack keystone / ... ?)
    :type authurl : str
    :param container_name: name of the container on which write the data
    :type container_name: str
    :param file_name: the original file name
    :type file_name : str
    :param application: Description of the application where the data
    come from or whatever you want
    :type application : str
    :param content_type: MIME Type of the data
    :type content_type : str
    :param mongodb_url: the MongoDB IP_ADDR with Port
    :type mongodb_url : str
    '''
    conn = swiftclient.Connection(user=user, key=key,
                                  authurl=authurl)
    client = MongoClient(mongodb_url)
    db = client.swift
    coll = db[container_name]
    if content_type is not None:
        # TODO : Check MIME type
        pass
    meta_data = {}
    if content_type is not None:
        meta_data["content_type"] = content_type
    else:
        meta_data["content_type"] = "None"
    meta_data["swift_user"] = user
    meta_data["swift_container"] = container_name
    meta_data["swift_object_id"] = str(get_id(mongodb_url))
    if application is not None:
        meta_data["application"] = application
    else:
        meta_data["application"] = user + "_" + container_name
    if file_name is not None:
        meta_data["swift_object_name"] = file_name
    meta_data["creation_date"] = datetime.datetime.now()
    meta_data["last_modified"] = datetime.datetime.now()
    meta_data["successful_operations"] = []
    meta_data["failed_operations"] = []
    if meta_data is not None :
        meta_data["other_data"] = other_data
    print(meta_data)

    if SwiftService({}).stat(container_name)["object"] is None:
        conn.put_container(container_name)
    retry = 0
    while True:
        try:
            conn.put_object(container_name, meta_data["swift_object_id"],
                            contents=file_content,
                            content_type=meta_data["content_type"])#,
            # headers={"x-webhook":"yes"})
            # Insert metadata over the data : only if data has been put
            coll.insert_one(meta_data)
            # client.stats.swift.update_one({"type": "data_to_process_list"},
            #                               {"$push":
            #                                   {
            #                                       "data_to_process": {
            #                                           "swift_id": meta_data[
            #                                               "swift_object_id"],
            #                                           "swift_container":
            #                                               meta_data[
            #                                                   "swift_container"],
            #                                           "swift_user": meta_data[
            #                                               "swift_user"],
            #                                           "content_type":
            #                                               meta_data[
            #                                                   "content_type"]
            #                                       }
            #                                   }
            #                               }
            #                               )
            return None
        except Exception as e:
            print(e)
            retry += 1
            if retry > 3:
                return None



@cross_origin(supports_credentials=True)
@app.route('/upload_file', methods=['POST'])
def upload_file():
    user = 'test:tester'
    key = 'testing'
    authurl = "http://127.0.0.1:8080/auth/v1.0"
    container_name= "test_ui-react"
    # check if the post request has the file part
    if 'file' not in request.files:
        return "No file to upload"
        #return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':

        return "No file selected"
    if file:
        filename = secure_filename(file.filename)
        # upload in openstack swift / mongodb
        insert_datalake(file, user, key, authurl, container_name,
                        application="UI-react_test",
                        content_type= file.content_type,
                        mongodb_url="127.0.0.1:27017",
                        )

        print(file.filename)
        print(file.name)
        print(file.content_type)
        print(file.content_length)
        print(file.headers)

        return "File uploaded"
    return "Error"


@cross_origin()
@app.route('/sensors_data', methods=['GET'])
def get_influx_data_sensor(org="test", bucket="test"):

    influx_client = InfluxDBClient(url="http://localhost:9999",
                                   token="nfd23prECgPsUjNkwPZ95L6sw74u5dNAwUy2ChMp9giyD_Bor7Hbnvp3W1hMaqN2Qrk0J_oyaIUtpZpcEXcohQ==",
                                                 org=org)
    query_api = influx_client.query_api()
    query = 'from(bucket:"test")|> range(start: -141400080m)|> group() |> filter(fn:(r) => r._measurement == "humidity")' \
            '|> filter(fn:(r) => r.uri == "u4/302/humidity/ilot2")'
    result = query_api.query(org=org, query=query)
    results = {}
    aux = 0
    val_min = None
    val_max = None
    for table in result:
        for record in table.records:
            if record["uri"] not in results:
                results[record["uri"]]={"id":record["uri"],"values":[{"val_min":val_min, "val_max":val_max}]}
            results[record["uri"]]["values"].append({"value":record.get_value(),"value_unit": record["value_units"], "date":datetime.datetime.timestamp(record["_time"]) })
            if val_max is None or record.get_value() > val_max :
                val_max = record.get_value()
            if val_min is None or record.get_value()<val_min:
                val_min = record.get_value()
    for uri in results:
        results[uri]["values"][0]["val_min"]=val_min
        results[uri]["values"][0]["val_max"]=val_max
    return build_actual_response(jsonify(results))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')