from sanic import Sanic
from sanic import response
import motor.motor_asyncio
from bson.objectid import ObjectId

app = Sanic(__name__)

class MotorHandler(object):

    _connection = None
    _db = None
    _collection = None

    async def get_connection(self):
        if self._connection is None:
            self._connection = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

        return self._connection

    async def set_db_and_collection(self, db_name, collection_name):
        conn = await self.get_connection()
        self._db = conn[db_name]
        self._collection = self._db[collection_name]

    async def insert(self, data):
        collection = self._collection
        ret = await collection.insert_one(data)
        return ret

    async def findById(self, id):
        collection = self._collection
        ret = await collection.find_one({'_id': ObjectId(id)})
        return ret


mongoHandler = MotorHandler()

@app.listener('after_server_start')
async def notify_mongo_started(app, loop):
    await mongoHandler.get_connection()
    await mongoHandler.set_db_and_collection('beepaste', 'texts')

@app.route("/save", methods=['POST'])
async def save(request):
    body = request.json
    ret = await mongoHandler.insert(body)
    return response.json(
        {'id': str(ret.inserted_id)},
        status=201
    )

@app.route("/fetch", methods=['POST'])
async def fetch(request):
    body = request.json['id']
    ret = await mongoHandler.findById(body)
    return response.json(
        {'id': str(ret['_id']), 'text': str(ret['text'])}
    )

app.run(host="0.0.0.0", port=8081, debug=False, log_config=None)
