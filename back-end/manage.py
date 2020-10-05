import os
import requests
from flask import Flask, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            url = request.form['url']
            r = requests.get(url)
            print(r.text)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('index.html')


# state = "IDLE"
#
#
# class ISBN(Resource):
#     def get(self):
#         return {'about': 'Hello World!'}
#
#     def post(self):
#         some_json = request.get_json()
#         return {'you sent': some_json}, 201


# class Multi(Resource):
#     def get(self, num):
#         return {'result': num*10}

# api.add_resource(ISBN, '/')
# api.add_resource(Multi, '/multi/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)
