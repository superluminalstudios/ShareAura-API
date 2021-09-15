from flask import Flask, request, jsonify
import pymongo, os
from dotenv import load_dotenv
import dns
from datetime import date
import wolframalpha
from bson.objectid import ObjectId

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
    query = {"items": {"$regex": item}}
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
    firstItem = items.split("+")[0]
    if 'TB' in firstItem:
        itemtype = "textbook"
    elif 'CW' in firstItem:
        itemtype = "notebook"
    else:
        itemtype = "stationary"
    data = {
        "username": username,
        "usernumber": usernumber,
        "itemtype": itemtype,
        "items": items,
    }
    collection.insert_one(data)
    response = jsonify("data")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


# Add Question
@app.route("/addquestion/<username>/<question>/<desc>", methods=["GET"])
def addQuestion(username="", question="", desc=""):
    client = wolframalpha.Client('34U93P-WGR36VG7WE')
    res = client.query(question)
    try:
	    answer = (next(res.results).text)
    except:
        res = 0
    
    if res == 0:
        data = {
            "datatype": "question",
            "username": str(username),
            "question": str(question),
            "desc": str(desc),
            "date": str(date.today().strftime("%B %d, %Y")),
            "comments": []
        }
    else:
        data = {
            "datatype": "question",
            "username": str(username),
            "question": str(question),
            "desc": str(desc),
            "date": str(date.today().strftime("%B %d, %Y")),
            "comments": [{
                "answer": str(answer),
                "username": "Clyde"
            }]
        }
    response = jsonify(data)
    collection.insert_one(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


# Show Questions
@app.route("/showquestions/<times>")
def showQuestions(times=""):
    query = {"datatype": {"$regex": "question"}}
    result = collection.find(query).limit(int(times)).sort("_id", -1)
    data = {}
    for item in result:
        item['_id'] = str(item['_id'])
        data[item['_id']] = item
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


# Add Answer
@app.route("/addanswer/<username>/<idVal>/<answer>")
def addAnswer(username="", idVal="", answer=""):
    print(username, idVal, answer)
    newAns = {'answer': answer, 'username': username}
    collection.update_one({"_id": ObjectId(idVal)},
                          {'$push': {
                              'comments': newAns
                          }})
    response = jsonify(newAns)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
