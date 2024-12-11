from re import I
import arrow
import configparser
import logging
import os

from bson.json_util import dumps, loads
from flask import Flask, jsonify, redirect, render_template, request, url_for, Response
from pymongo import MongoClient

import acp_times  # Brevet time calculations

import csv

from io import StringIO

###
# Globals
###
app = Flask(__name__)

# Load configuration (https://docs.python.org/3/library/configparser.html)
CONFIG = configparser.ConfigParser()
CONFIG.read("app.ini")


# Connect to MongoDB (update as needed)
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
if mongo_uri:
    client = MongoClient(mongo_uri)
else:
    client = MongoClient("localhost", 27017)
db = client.brevetdb
collection = db['brevetsdb']

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    """Redirect to the main brevet calculator page."""
    app.logger.debug("Main page entry")
    return render_template("calc.html")


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    app.logger.debug("Page not found")
    return render_template("404.html"), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    # Format: { km: km, begin_date: begin_date, begin_time: begin_time, distance: distance }
    dist_km = request.args.get("dist_km", -1, type=float)
    brevet_dist_km = request.args.get("distance", -1, type=int)
    begin_date = request.args.get("begin_date", "0000-00-00", type=str)
    begin_time = request.args.get("begin_time", "00:00", type=str)

    # Covert the start time to ISO 8601 format
    begin_ts = arrow.get(begin_date + " " + begin_time, "YYYY-MM-DD HH:mm").isoformat()

    app.logger.debug(
        f"request.args: {request.args}, dist_km={dist_km}, begin_ts={begin_ts}"
    )
    try:
        open_time = acp_times.open_time(dist_km, brevet_dist_km, begin_ts)
        close_time = acp_times.close_time(dist_km, brevet_dist_km, begin_ts)
    except ValueError as err:
        message = str(err)
        app.logger.debug(f"ValueError: {message}")
        result = {"error": message}
        return jsonify(result=result)

    open_close = {"open": open_time, "close": close_time}
    app.logger.debug(f"result: {open_close}")
    return jsonify(result=open_close)


@app.route("/_store_times", methods=["POST"])
def store_times():
    data = request.get_json()
    app.logger.debug(f"Data: {str(data)}")
    for item in data:
        item_doc = {
            "km": item["km"],
            "begin_date": item["begin_date"],
            "begin_time": item["begin_time"],
            "distance": item["distance"],
            "open": item["open"],
            "close": item["close"],
        }
        db.brevetdb.insert_one(item_doc)
    return jsonify({"message": "Times stored successfully!"}), 201


@app.route("/display_times")
def display_times():
    items = list(db.brevetdb.find())
    for item in items:
        item["_id"] = str(item["_id"])
    app.logger.debug(f"Items: {items}")
    return render_template("display_times.html", items=items)


### In my test I wasn't able to access the methods through ./list_api so I will add my methods here to uncomment if they dont work
'''
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

@app.route("/listAll")
def list_All():
    top = request.args.get('top', default=None, type=int)
    results = list(collection.find())
    if top:
        results = results[:top]

    if "/csv" in request.path:
        csv_output = to_csv(results)
        return Response(csv_output, mimetype='text/csv')
    return jsonify(results)
@app.route("/listAll/json")
def list_All_to_json():
    top = request.args.get('top', default=None, type=int)
    results = list(collection.find())
    if top:
        results = results[:top]

    if "/csv" in request.path:
        csv_output = to_csv(results)
        return Response(csv_output, mimetype='text/csv')
    return jsonify(results)
@app.route("/listAll/csv")
def list_All_to_csv():
    top = request.args.get('top', default=None, type=int)
    results = list(collection.find())
    if top:
        results = results[:top]

    csv_output = to_csv(results)
    return Response(csv_output, mimetype='text/csv')

@app.route("/listOpenOnly")
def list_Open_Only():
    top = request.args.get('top', default=None, type=int)
    results = list(collection.find({}, {'_id': 0, 'open': 1}).sort('open', 1))
    open_times = [item['open'] for item in results if 'open' in item]
    if top:
        open_times = open_times[:top]

    if "/csv" in request.path:
        csv_output = to_csv(open_times)
        return Response(csv_output, mimetype='text/csv')
    return jsonify(open_times)
@app.route("/listOpenOnly/json")
def list_Open_Only_to_json():
    top = request.args.get('top', default=None, type=int)
    results = list(collection.find({}, {'_id': 0, 'open': 1}).sort('open', 1))
    open_times = [item['open'] for item in results if 'open' in item]
    if top:
        open_times = open_times[:top]

    if "/csv" in request.path:
        csv_output = to_csv(open_times)
        return Response(csv_output, mimetype='text/csv')
    return jsonify(open_times)
@app.route("/listOpenOnly/csv")
def list_Open_Only_to_csv():
    top = request.args.get('top', default=None, type=int)
    results = list(collection.find({}, {'_id': 0, 'open': 1}).sort('open', 1))
    open_times = [item['open'] for item in results if 'open' in item]
    if top:
        open_times = open_times[:top]

    csv_output = to_csv(open_times)
    return Response(csv_output, mimetype='text/csv')

@app.route("/listCloseOnly")
def list_Close_Only():
    top = request.args.get('top', default=None, type=int)
    results = list(collection.find({}, {'_id': 0, 'close': 1}).sort('close', 1))
    close_times = [item['close'] for item in results if 'close' in item]
    if top:
        close_times = close_times[:top]

    if "/csv" in request.path:
        csv_output = to_csv(close_times)
        return Response(csv_output, mimetype='text/csv')
    return jsonify(close_times)
@app.route("/listCloseOnly/json")
def list_Close_Only():
    top = request.args.get('top', default=None, type=int)
    results = list(collection.find({}, {'_id': 0, 'close': 1}).sort('close', 1))
    close_times = [item['close'] for item in results if 'close' in item]
    if top:
        close_times = close_times[:top]

    if "/csv" in request.path:
        csv_output = to_csv(close_times)
        return Response(csv_output, mimetype='text/csv')
    return jsonify(close_times)
@app.route("/listCloseOnly/csv")
def list_Close_Only():
    top = request.args.get('top', default=None, type=int)
    results = list(collection.find({}, {'_id': 0, 'close': 1}).sort('close', 1))
    close_times = [item['close'] for item in results if 'close' in item]
    if top:
        close_times = close_times[:top]

    csv_output = to_csv(close_times)
    return Response(csv_output, mimetype='text/csv')
'''

#############

app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.logger.debug(f"Opening for global access on port {CONFIG['server']['port']}")
    app.run(port=CONFIG["server"]["port"], host="0.0.0.0", debug=True)