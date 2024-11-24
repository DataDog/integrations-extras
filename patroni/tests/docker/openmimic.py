from flask import Flask, Response, send_file

app = Flask(__name__)


@app.route("/metrics")
def passResponse():
    return send_file("metrics.txt")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
