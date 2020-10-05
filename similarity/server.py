import time
from flask import Flask, request, jsonify
import bz2
import ast
from similarity_ranking import SimilarityRanking
import global_data

app = Flask(__name__)

global_data.state = "IDLE"
global_data.proc = None


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        if global_data.state == "IDLE":
            try:
                # decompress data and write to file
                bz2_data = request.data
                bookTitles = bz2.decompress(bz2_data)
                bookTitleList = ast.literal_eval(bookTitles.decode("utf-8"))
                with open("book_titles.txt", "w") as Of:
                    for book in bookTitleList:
                        Of.write(book + '\n')
                Of.close()

                # load model
                global_data.similarityRanker = SimilarityRanking()
                global_data.proc = global_data.similarityRanker.loadModel('model.bin', 'book_titles.txt', '30')

                # add 15 seconds delay for the model to be loaded
                time.sleep(15)
                global_data.state = "READY"
                return jsonify({'status': 'finish loading model'})
            except:
                errors.append(
                    "Error Occur"
                )
            return jsonify({'status': 'book titles received'})
        elif global_data.state == "READY":
            try:
                req = request.get_json()
                if "search-text" in req:
                    searchText = req["search-text"]
                    lines = global_data.similarityRanker.similarityRanking(global_data.proc, searchText)
                    json = global_data.similarityRanker.filterBookTitleRanking(lines)
                    return jsonify(json)
                elif "command" in req:
                    cmd = req["command"]
                    if cmd == "EXIT":
                        global_data.similarityRanker.terminateProc(global_data.proc)
                        # add 5 seconds delay for the model to be unloaded
                        time.sleep(5)
                        global_data.state = "IDLE"
                        return jsonify({'status': 'finish search session'})
                    return jsonify({'message': '?'})
            except:
                errors.append(
                    "Error Occur"
                )

if __name__ == '__main__':
    app.run(debug=True)
