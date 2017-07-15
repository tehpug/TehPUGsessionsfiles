import json
from pymongo import MongoClient

from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.resource import Resource

client = MongoClient('mongodb://localhost:27017/')
db = client['benchmarkdb']
collection = db['bcollection']


class Save(Resource):

    def render_POST(self, request):
        text = json.loads(request.content.getvalue())
        retData = collection.insert_one(text).inserted_id
        return json.dumps({'id': str(retData)})

    
class Fetch(Resource):

    def render_POST(self, request):
        text = json.loads(request.content.getvalue())
        retData = collection.find_one(text)
        data = str(retData)
        return json.dumps(data)


root = Resource()
root.putChild("save", Save())
root.putChild("fetch", Fetch())
factory = Site(root)
reactor.listenTCP(8083, factory)
reactor.run()
