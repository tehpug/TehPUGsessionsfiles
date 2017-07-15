import base64

from bottle import run, route, request


@route('/encode', method='POST')
def encode():
    text = request.json
    retData = base64.b64encode(text['text'].encode('utf-8')).decode('utf-8')
    return {'encoded': retData}


@route('/decode', method='POST')
def decode():
    text = request.json
    retData = base64.b64decode(text['text'].encode('utf-8')).decode('utf-8')
    return {'decoded': retData}


run(host='localhost', port=8083, debug=True, reloader=True)
