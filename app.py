
import json
import flask
import pandas as pd


app = flask.Flask(__name__)


@app.route("/")
def index():
    data = pd.read_csv("data.txt").values
    return flask.render_template("index.html", data=data)


@app.route("/details/<airport>")
def details(airport):

    with open('history.json') as f:
        history = json.load(f)

    return flask.render_template("details.html", data=history[airport],
                                 airport=airport)


if __name__ == "__main__":
    port = 5075
    app.run(host='83.220.168.38', port=port)
