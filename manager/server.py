from flask import Flask, request, jsonify
from MongoDB.query import MarcQuery
from datetime import datetime
import sys
import requests
import global_data
import json
import os

app = Flask(__name__)
CFG_INI = "./config.ini"

def log(str):
    print(str, file=sys.stderr)

# avoid CORS problem: https://stackoverflow.com/questions/26980713/solve-cross-origin-resource-sharing-with-flask
def enableCORS(js):
    response = jsonify(js)
    response.headers.add('Access-Control-Allow-Origin', '*')
    log("CORS enabled")
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    if request.method == "POST":
        try:
            if global_data.state == "IDLE":
                log("received ISBN list string: Time = "+datetime.now().strftime("%H:%M:%S"))
                # convert bytes object to string
                isbnString = request.data.decode(encoding='UTF-8')
                global_data.marcQuery = MarcQuery(CFG_INI)
                bookListString = global_data.marcQuery.getRelatedBookRecordsFromBorrowRecords(isbnString)
                log("get the related book records and send the list to AI server: Time = "+
                      datetime.now().strftime("%H:%M:%S"))

                log("AI_SERVER_ADDRESS: " + os.environ['AI_SERVER_ADDRESS'])

                r = requests.post(url=os.environ['AI_SERVER_ADDRESS'], data=bookListString, timeout=40)
                log("get back the response from AI server: Time ="+datetime.now().strftime("%H:%M:%S"))
                if r.ok == True:
                    global_data.state = "READY"
                    return enableCORS(json.loads(r.text))

            elif global_data.state == "READY":
                r = requests.post(url=os.environ['AI_SERVER_ADDRESS'],
                                  data=request.data,
                                  timeout=40)
                if r.ok == True:
                    res = json.loads(r.text)
                    if "status" in res:
                        status = json.loads(r.text).get("status")
                        if status == "finish search session":
                            global_data.state = "IDLE"
                    return enableCORS(json.loads(r.text))
        except:
            errors.append(
                {
                    "state": global_data.state,
                    "error": "unknown Error",
                    "request": "POST"
                }
            )

    elif request.method == "GET":
        return enableCORS(
            {
                'message': 'Manager status',
                'state': global_data.state
            })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2354, debug=True)
