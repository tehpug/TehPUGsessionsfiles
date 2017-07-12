from sanic import Sanic
from sanic import response
import base64

app = Sanic(__name__)

@app.route("/encode", methods=['POST'])
async def encoder(request):
    body = request.json['text']
    retData = base64.b64encode(body.encode('utf-8')).decode('utf-8')
    return response.json(
        {'encoded': retData}
    )

@app.route("/decode", methods=['POST'])
async def decoder(request):
    body = request.json['text']
    retData = base64.b64decode(body.encode('utf-8')).decode('utf-8')
    return response.json(
        {'decoded': retData}
    )

app.run(host="0.0.0.0", port=8081, debug=False, log_config=None)
