from flask import Flask, render_template, request
import main, json
from Module import module3_1

app = Flask(__name__)


@app.route("/")
def index():
    # return render_template('results.html')
    return render_template('index.html')


@app.route("/search", methods=['POST'])
def search():
    search_query = request.form['search']
    seuil = request.form['seuil']
    filtre = request.form['filtre']  # Récuperation de la valeur du radio button

    request_type = 0 if filtre == 'actors' else 1
    print('you searched ' + search_query + " " + filtre + 'With ratio = ' + seuil)
    search_res = main.DoSearch(search_query + " " + filtre, float(seuil))
    search_res["search"] = search_query
    print(str(search_res).encode('utf-8', 'ignore'))
    return render_template('results.html', results=search_res, type=request_type)


@app.route("/test")
def test():
    res = main.DoSearch("")
    return render_template('results.html', matrice=res["matrice"], targets=json.dumps(res["target"]))


if __name__ == "__main__":
    app.debug = True
    app.run()
