﻿from flask import Flask, render_template
import main

app = Flask(__name__)


@app.route("/search/<search>")
def search(search):
    print('you searched '+search)
    search_res = main.DoSearch(search)
    return render_template('search.html', search=search)

if __name__ == "__main__":
    app.run()
