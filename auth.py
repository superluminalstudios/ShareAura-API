from replit import db
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/signup/<phone>/<password>", methods=["GET"])
def signUp(phone=0,password=0):
  phone, password = str(phone), str(password)
  try:
    db[phone] = password
    response = jsonify({"proceed":"True"})
  except:
    response = jsonify({"proceed":"False"})
  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add("Access-Control-Allow-Headers", "*")
  response.headers.add("Access-Control-Allow-Methods", "*")
  return response




@app.route("/signin/<phone>/<password>", methods=["GET"])
def signIn(phone=0,password=0):
  phone, password = str(phone), str(password)
  try:
    match = db.prefix(phone)
    match = str(match[0])
    value=db[match]
    stored_password = value.split('-break-', 1)[1]
    full_name = value.replace(stored_password, '')
    full_name = full_name.replace('-break-', '')
    if stored_password == password:
      response = jsonify({"proceed" : "True", "name": full_name})
    else:
      response = jsonify({"proceed":"False"})
  except:
    response = jsonify("False")
  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add("Access-Control-Allow-Headers", "*")
  response.headers.add("Access-Control-Allow-Methods", "*")
  return response
  
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
