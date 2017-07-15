import base64

from flask import Flask, jsonify, request

app = Flask('__main__')

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/encode', methods=['POST'])
def encode():
    text = request.json['text']
    retData = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return jsonify({'encoded': retData})


@app.route('/decode', methods=['POST'])
def decode():
    text = request.json['text']
    retData = base64.b64decode(text.encode('utf-8')).decode('utf-8')
    return jsonify({'decoded': retData})

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port= 8082, debug=False)
