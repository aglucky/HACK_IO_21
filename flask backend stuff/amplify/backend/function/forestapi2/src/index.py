import awsgi
from flask_cors import CORS
from flask import Flask, json, jsonify, request
import boto3
import os
import time
import json
import openai

 
app = Flask(__name__)
CORS(app)
client = boto3.client("dynamodb")
TABLE = os.environ.get("STORAGE_FORESTDB_NAME")
BASE_ROUTE="/api2"
app.config['JSON_SORT_KEYS'] = False
OPENAI_KEY = os.environ.get("OPENAI_KEY")
openai.api_key = os.getenv(OPENAI_KEY)

def boto3_db_fetch():
    global TABLE
    return client.scan(TableName=TABLE)


def create_geojson():
    featuresArray = []
    BASE_MAPBOX_DICTIONARY = {
        'type': 'geojson',
        'data': {
        'type': 'FeatureCollection',
        'features': featuresArray}}
    bodo3_dict = boto3_db_fetch()
    dataDict = bodo3_dict
    databaseTableDict = dataDict
    databaseTable = databaseTableDict["Items"]
    print(databaseTable)
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
    print(BASE_MAPBOX_DICTIONARY)

    return(BASE_MAPBOX_DICTIONARY)


@app.route(BASE_ROUTE+"/getMapData", methods=['GET'])
def index():
    return jsonify(create_geojson())
@app.route(BASE_ROUTE+"/getData", methods=['GET'])
def getIndex():
    return jsonify(data=str(boto3_db_fetch()))


@app.route(BASE_ROUTE+"/openaiPostData", methods=['POST'])
def openai_post():
    value = request.get_json(force=True)
    #prompt = request.form[]
    '''
    response = openai.Completion.create(
    engine="davinci",
    prompt=f"{prompt}\n\n\ntl;dr single point for future:",
    temperature=0.23,
    max_tokens=60,
    top_p=0.95,
    frequency_penalty=0.19,
    presence_penalty=0,
    stop=["."])
    returnValue = response.to_dict()["choices"][0]["text"]
    return returnValue
    '''
    return value
@app.route(BASE_ROUTE+"/classifierPostData", methods=['POST'])
def classifierPost():
    pass


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