from flask import Flask, jsonify, request, Response
from flask_restful import Resource, Api
import pymongo

import csv

from io import StringIO

# Instantiate the app
app = Flask(__name__)
api = Api(app)

# MongoDB Configuration
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['brevets']
collection = db['brevetsdb']

def to_csv(data):
    output = StringIO()
    writer = csv.writer(output)

    if isinstance(data, list) and data and isinstance(data[0]. dict):
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())
    else:
        writer.writerow(["data"])
        for item in data:
            writer.writerow([item])

    return output.getvalue()

class ListAll(Resource):
    def get(self):
        top = request.args.get('top', default=None, type=int)
        results = list(collection.find())
        if top:
            results = results[:top]

        if "/csv" in request.path:
            csv_output = to_csv(results)
            return Response(csv_output, mimetype='text/csv')
        return jsonify(results)

class ListOpenOnly(Resource):
    def get(self):
        top = request.args.get('top', default=None, type=int)
        results = list(collection.find({}, {'_id': 0, 'open': 1}).sort('open', 1))
        open_times = [item['open'] for item in results if 'open' in item]
        if top:
            open_times = open_times[:top]

        if "/csv" in request.path:
            csv_output = to_csv(open_times)
            return Response(csv_output, mimetype='text/csv')
        return jsonify(open_times)

class ListCloseOnly(Resource):
    def get(self):
        top = request.args.get('top', default=None, type=int)
        results = list(collection.find({}, {'_id': 0, 'close': 1}).sort('close', 1))
        close_times = [item['close'] for item in results if 'close' in item]
        if top:
            close_times = close_times[:top]

        if "/csv" in request.path:
            csv_output = to_csv(close_times)
            return Response(csv_output, mimetype='text/csv')
        return jsonify(close_times)

# Create routes
api.add_resource(ListAll, '/listAll', '/listAll/json', '/listAll/csv')
api.add_resource(ListOpenOnly, '/listOpenOnly', '/listOpenOnly/json', '/listOpenOnly/csv')
api.add_resource(ListCloseOnly, '/listCloseOnly', '/listCloseOnly/json', '/listCloseOnly/csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)