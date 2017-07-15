from japronto import Application
import motor.motor_asyncio
from bson.objectid import ObjectId

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
inited = 0

async def save(request):
    global inited
    if not inited:
        await mongoHandler.get_connection()
        await mongoHandler.set_db_and_collection('beepaste', 'texts')
        inited = 1

    body = request.json
    ret = await mongoHandler.insert(body)
    return request.Response(
        json={'id': str(ret.inserted_id)})

async def fetch(request):
    global inited
    if not inited:
        await mongoHandler.get_connection()
        await mongoHandler.set_db_and_collection('beepaste', 'texts')
        inited = 1

    body = request.json['id']
    ret = await mongoHandler.findById(body)
    return request.Response(
        json={'id': str(ret['_id']), 'text': str(ret['text'])})


app = Application()
r = app.router

r.add_route('/save', save, methods=['POST'])
r.add_route('/fetch', fetch, methods=['POST'])

app.run(port=8080)
