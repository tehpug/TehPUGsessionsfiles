from flask import Flask, jsonify, request

from data_model import DataModel
from mongoengine import connect

app = Flask('__main__')

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


connect(host="mongodb://localhost:27017/beepaste")

@app.route('/save', methods=['POST'])
def save():
    body = request.json
    new_data = DataModel(**body)
    ret = new_data.save()
    return jsonify({'id': str(ret.id)})


@app.route('/fetch', methods=['POST'])
def fetch():
    body = request.json['id']
    ret = DataModel.objects(id=body).first()
    return jsonify({'id': str(ret.id), 'text': ret.text})

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port= 8082, debug=False)
