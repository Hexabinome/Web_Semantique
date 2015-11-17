from flask import Flask

app = Flask(__name__)


@app.route("/search/<search>")
def search(search):
    print('you searched '+search)
    return 'bite'

if __name__ == "__main__":
    app.run()
