import json

from flask import Flask, render_template, request, Response
import main, time

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

'''
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
        search_res = main.DoSearch(search_query + " " + type, float(seuil), request_type)
    elif request_filtre == 1:
        search_res = main.DoSimilar(search_query + " " + type, float(seuil), request_type)
    search_res["search"] = search_query

    print(str(search_res).encode('utf-8', 'ignore'))
    return render_template('results.html', results=search_res, type=request_type)
'''

@app.route("/test")
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
        search_res = main.DoSearch(search_query + " " + type, float(seuil), request_type)
    elif request_filtre == 1:
        search_res = main.DoSimilar(search_query + " " + type, float(seuil), request_type)

    search_res["search"] = search_query

    print(str(search_res).encode('utf-8', 'ignore'))

    return render_template('results.html', results=search_res, type=request_type)


'''
@app.route('/loading')
def loading():
    for i in range(100):
        progress(test)
        time.sleep(0.2)

@app.route('/progress')
def progress(test):
    def generate(test):
        print(test)
    return Response(generate(), mimetype= 'text/event-stream')
'''
    #def generate():
    #    x = 0
    #    while x < 100:
    #        print(x)
    #        x = x + 10
    #        time.sleep(0.2)
    #        yield "data:" + str(x) + "\n\n"
    #return Response(generate(), mimetype= 'text/event-stream')

if __name__ == "__main__":
    app.debug = True
    app.run()
