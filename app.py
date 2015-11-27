import json

from flask import Flask, render_template, request, Response
import main, time

app = Flask(__name__)


@app.route("/old")
def index():
    return render_template('index.html')

@app.route("/")
def test():
    return render_template('curtain.html')

@app.route("/search", methods=['POST'])
def search():
    search_query = request.form['search']
    seuil = request.form['seuil']
    type = request.form['type']  # Récuperation de la valeur du radio button
    filtre = request.form['filtre']

    request_filtre = 0 if filtre == 'memento' else 1
    request_type = 0 if type == 'actors' else 1

    print('you searched ', search_query, " ", type, 'With ratio = ', seuil, "With filter : ", request_filtre)

    if request_filtre == 0:
        search_res = main.DoSearch(search_query + " " + (type if type == 'actors' else ""), float(seuil), request_type)
    elif request_filtre == 1:
        search_res = main.DoSimilar(search_query, float(seuil), request_type)

    search_res["search"] = search_query
    search_res["type"] = request_type

    print("fin call main", str(search_res).encode('utf-8', 'ignore'))

    return json.dumps(search_res)


if __name__ == "__main__":
    app.debug = True
    app.run()
