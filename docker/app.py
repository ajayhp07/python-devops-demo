from flask import Flask, jsonify, render_template
from prometheus_client import Counter, generate_latest
import socket
import datetime

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

@app.before_request
def before_request():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()

@app.route("/")
def home():
    return render_template(
        "index.html",
        hostname=socket.gethostname(),
        time=datetime.datetime.now()
    )

@app.route("/health")
def health():
    return jsonify(status="OK"), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200



if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000)

