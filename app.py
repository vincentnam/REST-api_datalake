
from flask import Flask, request, jsonify, make_response, flash
from werkzeug.utils import secure_filename

import sys
app = Flask(__name__)

UPLOAD_FOLDER = "/datalake/flask_tmp"
globals()["INFLUXDB_URI"] = "http://141.115.103.33:9999"
globals()["SWIFT_URI"] = "http://141.115.103.30"


import sys

import logging
import os
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')



@app.route('/upload_file', methods=['POST'])
def upload_file():
    logger.info("welcome to upload`")
    user = 'test:tester'
    key = 'testing'
    authurl = globals()["SWIFT_URI"] + ":8080/auth/v1.0"
    container_name = "test_ui-react"
    # check if the post request has the file part
    logger.info(str(type(request.files["file"])))
    if 'file' not in request.files:
        return jsonify(message="No file to upload")
    file = request.files["file"]

    if file.filename == '':
        flash('No selected file')
        return "No file"
    if file.filename != 'savehistor':
        return "PAS BON"
    print('This is error output', file=sys.stderr, flush=True)
    print('This is standard output', file=sys.stdout, flush=True)
    app.logger.info(type(file))
    filename = secure_filename(file.filename)

    f = open(filename, "w+")
    f.write(file)

    return jsonify(message="Ok")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)