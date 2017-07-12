import base64
import json

from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.resource import Resource


class Encode(Resource):

    def render_POST(self, request):
        text = json.loads(request.content.getvalue())
        retData = base64.b64encode(text['text'].encode('utf-8')).decode('utf-8')
        return json.dumps({'encoded': retData})


class Decode(Resource):

    def render_POST(self, request):
        text = json.loads(request.content.getvalue())
        retData = base64.b64decode(text['text'].encode('utf-8')).decode('utf-8')
        return json.dumps({'decoded': retData})


root = Resource()
root.putChild("encode", Encode())
root.putChild("decode", Decode())
factory = Site(root)
reactor.listenTCP(8083, factory)
reactor.run()
