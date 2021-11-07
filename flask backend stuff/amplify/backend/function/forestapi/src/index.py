import awsgi
from flask_cors import CORS
from flask import Flask, json, jsonify, request
import boto3
import os
import time
 
app = Flask(__name__)
CORS(app)

client = boto3.client("dynamodb")

BASE_ROUTE="/api"

@app.route(BASE_ROUTE+"/getData", methods=['GET'])
def index():
    return jsonify(message="Hello, World!")

@app.route(BASE_ROUTE+"/postData", methods=['POST'])
def postData(request):
    return 200
    

def handler(event, context):
    return awsgi.response(app, event, context)