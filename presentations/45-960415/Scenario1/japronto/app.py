from japronto import Application
import base64

async def encoder(request):
    body = request.json['text']
    retData = base64.b64encode(body.encode('utf-8')).decode('utf-8')
    return request.Response(
        json={'encoded': retData})

async def decoder(request):
    body = request.json['text']
    retData = base64.b64decode(body.encode('utf-8')).decode('utf-8')
    return request.Response(
        json={'decoded': retData})


app = Application()
r = app.router

r.add_route('/encode', encoder, methods=['POST'])
r.add_route('/decode', decoder, methods=['POST'])

app.run(port=8080)
