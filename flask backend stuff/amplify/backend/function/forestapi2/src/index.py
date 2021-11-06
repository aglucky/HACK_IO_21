import awsgi
from flask_cors import CORS
from flask import Flask, json, jsonify, request
import boto3
import os
import time
 
app = Flask(__name__)
CORS(app)

client = boto3.client("dynamodb")
TABLE = os.environ.get("STORAGE_FORESTDB_NAME")

BASE_ROUTE="/api2"

@app.route(BASE_ROUTE+"/getData", methods=['GET'])
def index():
    return jsonify(data=str(client.scan(TableName=TABLE)))

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