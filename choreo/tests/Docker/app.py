from flask import Flask, send_file

app = Flask(__name__)


@app.route('/metrics')
def serve_metrics():
    return send_file('metrics.txt', as_attachment=False)


if __name__ == '__main__':
    app.run()
