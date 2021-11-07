import awsgi
from flask_cors import CORS
from flask import Flask, json, jsonify, request
import boto3
import os
import time
import json

 
app = Flask(__name__)
CORS(app)
client = boto3.client("dynamodb")
TABLE = os.environ.get("STORAGE_FORESTDB_NAME")
featuresArray = []
BASE_MAPBOX_DICTIONARY = {
    'type': 'geojson',
    'data': {
    'type': 'FeatureCollection',
    'features': featuresArray}}

BASE_ROUTE="/api2"

def boto3_db_fetch():
    global TABLE
    return client.scan(TableName=TABLE)


def create_geojson():
    global BASE_MAPBOX_DICTIONARY
    global featuresArray
    bodo3_dict = boto3_db_fetch()
    dataDict = bodo3_dict
    databaseTableDict = dataDict
    databaseTable = databaseTableDict["Items"]
    for item in databaseTable:
        lat = item["lat"]["N"]
        lng = item["lng"]["N"]
        report = item["report"]["S"]
        BASE_GEOJSON_OBJECT = {
                                "type": "Feature",
                                "properties": {
                                "description":
                                "<strong>Accident Description</strong><p>"+report+"</p>"
                                },
                                "geometry": {
                                "type": "Point",
                                "coordinates": [lng, lat]
                                }
                            }
        featuresArray.append(BASE_GEOJSON_OBJECT)
    return BASE_MAPBOX_DICTIONARY


@app.route(BASE_ROUTE+"/getMapData", methods=['GET'])
def index():
    return create_geojson()
@app.route(BASE_ROUTE+"/getData", methods=['GET'])
def getIndex():
    return jsonify(data=str(boto3_db_fetch()))

@app.route(BASE_ROUTE+"/postData", methods=['POST'])
def postData():
    request_json = request.get_json()
    client.put_item(TableName=TABLE,Item={
        'time': {'N': str(time.time())},
        'lat': {'N': str(request_json.get("lat"))},
        'lng': {'N': str(request_json.get("lng"))},
        'report':{'S': str(request_json.get("report"))},
        'rearend': {'B': str(request_json.get('rearend'))}
    })
    return jsonify(message="Item created"),200
    

def handler(event, context):
    return awsgi.response(app, event, context)