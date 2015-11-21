from flask import Flask, render_template, request
import main

app = Flask(__name__)


@app.route("/")
def index():
    # return render_template('results.html')
    return render_template('index.html')


@app.route("/search", methods=['POST'])
def search():
    search = request.form['search']

    actor = " actor " if request.form.getlist('actors') == ['on'] else " "
    film = " movie " if request.form.getlist('films') == ['on'] else " "
    print('you searched ' + search + actor + film)
    search_res = main.DoSearch(search)
    return render_template('results.html', search=search_res)


if __name__ == "__main__":
    app.debug = True
    app.run()
