from flask import Flask, request, jsonify
import pymongo, os
from dotenv import load_dotenv
import dns
from datetime import datetime

# Connect to DB
load_dotenv()
MONGODB_URI = os.environ.get("MONGODB_URI")
client = pymongo.MongoClient(MONGODB_URI)
db = client.database
collection = db.requests


# Init webserver
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


# Categories
@app.route("/category/<cat>/<quantity>", methods=["GET"])
def mainPageCats(cat="textbook", quantity="3"):
    query = {"itemtype": {"$in": [cat]}}
    result = collection.find(query).limit(int(quantity)).sort("_id", -1)
    data = {}
    for item in result:
      item['_id'] = str(item['_id']) 
      data[item['_id']] = item
      item['itemList'] = item['items'].split("+")
      item['items'] = str(item['items']).replace("+", " · ")    
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response
    
# Search
@app.route("/search/<item>", methods=["GET"])
def searchRequests(item="Phy 11"):
    item = item.title()
    query = {"items": {"$regex" : item}}
    result = collection.find(query).limit(15).sort("_id", -1)
    data = {}
    for item in result:
      item['_id'] = str(item['_id']) 
      data[item['_id']] = item
      item['itemList'] = item['items'].split("+")
      item['items'] = str(item['items']).replace("+", " · ") 
      
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


# Add Req
@app.route("/add/<username>/<usernumber>/<items>", methods=["GET"])
def addRequest(username="", usernumber="", items=""):
    items.split("+")

    firstItem=items.split("+")[0]
    textbooks=['Maths 11', 'Chem 11', 'Phy 11', 'Bio 11', 'Applied Maths 11']

    if firstItem in textbooks:
      itemtype="textbook"
    elif 'CW' in firstItem:
      itemtype = "notebook"
    else:
      itemtype = "stationary"

    data = {
        "username":  username,
        "usernumber": usernumber,
        "itemtype": itemtype,
        "items": items,
        "date": datetime.now()
    }
    collection.insert_one(data)
    response = jsonify("data")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
