mport base64

from bottle import run, route, request

client = MongoClient('mongodb://localhost:27017/')
db = client['benchmarkdb']
collection = db['bcollection']


@route('/encode', method='POST')
def encode():
    text = request.json
    retData = collection.insert_one(text).inserted_id
    return {'id': str(retData)}


@route('/decode', method='POST')
def decode():
    text = request.json
    retData = collection.find_one(text)
    data = str(retData)
    return data


run(host='localhost', port=8083, debug=True, reloader=True)
