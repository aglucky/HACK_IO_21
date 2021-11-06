import awsgi
from flask_cors import CORS
from flask import Flask, json, jsonify, request
 
app = Flask(__name__)
CORS(app)


BASE_ROUTE="/api"

@app.route("/", methods=['GET'])
def index():
    return jsonify(message="Hello, World!")

def handler(event, context):
    return awsgi.response(app, event, context)