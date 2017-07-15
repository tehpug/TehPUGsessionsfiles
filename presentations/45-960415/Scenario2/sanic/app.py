from sanic import Sanic
from sanic import response
from data_model import DataModel
from SanicMongo import connect

app = Sanic(__name__)

@app.listener('after_server_start')
async def notify_mongo_started(app, loop):
    connect(host="mongodb://localhost:27017/beepaste")

@app.route("/save", methods=['POST'])
async def save(request):
    body = request.json
    new_data = DataModel(**body)
    ret = await new_data.save()
    return response.json(
        {'id': str(ret.id)},
        status=201
    )

@app.route("/fetch", methods=['POST'])
async def fetch(request):
    body = request.json['id']
    ret = await DataModel.objects(id=body).first()
    return response.json(
        {'id': str(ret.id), 'text': ret.text}
    )

app.run(host="0.0.0.0", port=8081, debug=False, log_config=None)
