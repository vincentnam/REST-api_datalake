import email.parser

from flask import Flask, request, jsonify, make_response, flash
from werkzeug.utils import secure_filename
from requests_toolbelt import MultipartEncoder
import sys
app = Flask(__name__)
from requests_toolbelt.multipart import decoder
UPLOAD_FOLDER = "/datalake/flask_tmp"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
globals()["INFLUXDB_URI"] = "http://141.115.103.33:9999"
globals()["SWIFT_URI"] = "http://141.115.103.30"
from flask_cors import CORS, cross_origin

# CORS(app)
from werkzeug.datastructures import ImmutableMultiDict


import sys

import logging
import os
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
    app.logger.debug('Body: %s', request.form)


#
# @cross_origin()
# @app.route('/upload_file', methods=['POST', 'OPTIONS'])
# def upload_file():
#     logger.info("welcome to upload`")
#     if request.method=="OPTIONS":
#         return jsonify(200)
#     if request.method=="POST":
#         return jsonify(201)
#     user = 'test:tester'
#     key = 'testing'
#     authurl = globals()["SWIFT_URI"] + ":8080/auth/v1.0"
#     container_name = "test_ui-react"
#     # check if the post request has the file part
#     logger.info(request.data)
#     #
#     # if 'file' not in request.files:
#     #     logger.info("welcome to upload zer`")
#     #
#     #     # logger.info(type(request.get_data()))
#     #     # logger.info(request.get_data(parse_form_data=True))
#     #     # logger.info(request.values)
#     #     # logger.info(request.make_form_data_parser())
#     #     # logger.info(request.headers.values())
#     #     # logger.info(request.headers)
#     #     # logger.info(type(request.headers))
#     #     multipart_string = "--ce560532019a77d83195f9e9873e16a1\r\nContent-Disposition: form-data; name=\"author\"\r\n\r\nJohn Smith\r\n--ce560532019a77d83195f9e9873e16a1\r\nContent-Disposition: form-data; name=\"file\"; filename=\"example2.txt\"\r\nContent-Type: text/plain\r\nExpires: 0\r\n\r\nHello World\r\n--ce560532019a77d83195f9e9873e16a1--\r\n"
#     #     content_type = "multipart/form-data; boundary=ce560532019a77d83195f9e9873e16a1"
#     #     # logger.info(decoder.MultipartDecoder(request.data))
#     #     #         msg = email.parser.BytesParser().parsebytes(request.data)
#     #     #         logger.info({ part.get_param('name', header='content-disposition'): part.get_payload(decode=True)
#     #     #     for part in msg.get_payload()
#     #     # })
#     #     # logger.info(request.get_json())
#     #     # encoder = MultipartEncoder(request.data)
#     #     # logger.info(encoder.to_string())
#     #     # for i in request.form.keys():
#     #     #     logger.info(i)
#     #     # logger.info(request.stream.read())
#     #     # logger.info(request.form.keys())
#     #     # f = open("test", "bw+")
#     #     # logger.info(len(request.files))
#     #     # f.write(request.get_data())
#     #     return jsonify((request.data.decode()))
#     # logger.info("welcome to upload zer`")
#     # try:
#     #     file = request.files["file"]
#     # except:
#     #     logger.info("qsdlmkqsd`")
#     #
#     # # logger.info(str(type(request.files["file"])))
#     # #
#     # # if file.filename == '':
#     # #     flash('No selected file')
#     # #     return "No file"
#     # # if file.filename != 'savehistor':
#     #
#     # #     return "PAS BON"
#     # # print('This is error output', file=sys.stderr, flush=True)
#     # # print('This is standard output', file=sys.stdout, flush=True)
#     # app.logger.info("Squiqui")
#     # filename = secure_filename(file.filename)
#     #
#     # file.save("/flask_tmp/test.txt")
#     # if request.method == 'POST':
#     #     dummy = request.form
#     # resp = make_response()
#     # resp.headers['Content-Type'] = "application/json"
#     # return make_response()
#     return jsonify(message="Ok")

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return jsonify("Pas file")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return jsonify("Pas ok")
        if file :
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify("Ok")
    return jsonify("OK")
if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)