from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "CI/CD Production Lab"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "broken"
    })

@app.route("/info")
def info():
    return jsonify({
        "service": "cicd-production-lab",
        "version": "1.0.0"
    })


@app.route("/version")
def version():
    return jsonify({
        "version": "1.0.0"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)