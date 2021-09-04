from flask import Flask, request, jsonify
import pymongo, os
from dotenv import load_dotenv
import dns

# Connect to DB
load_dotenv()
MONGODB_URI = os.environ.get("MONGODB_URI")
client = pymongo.MongoClient(MONGODB_URI)
db = client.database
collection = db.requests


# Init webserver
app = Flask(__name__)

# Categories
@app.route("/category/<cat>", methods=["GET"])
def mainPageCats(cat="textbook"):
    query = {"itemtype": {"$in": [cat]}}
    result = collection.find(query).limit(3)
    data = {}
    for item in result:
      item['_id'] = str(item['_id']) 
      data[item['_id']] = item
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response
    
# Search
@app.route("/search/<item>", methods=["GET"])
def searchRequests(item="Phy 11"):
    #item = item.title()
    query = {"items": {"$in": [item]}}
    result = collection.find(query).limit(15)
    data = {}
    for item in result:
      item['_id'] = str(item['_id']) 
      data[item['_id']] = item
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


# Add Req
@app.route("/add/<username>/<usernumber>/<itemtype>/<items>", methods=["GET"])
def addRequest(username="", usernumber="", itemtype="", items=""):
    items = items.split("+")
    data = {
        "username":  username,
        "usernumber": usernumber,
        "itemtype": itemtype,
        "items": items,
    }
    collection.insert_one(data)
    return "Added to DB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
# In Vue, name all items in Title Case
