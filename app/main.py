import logging
import os

from flask import Flask, jsonify

app = Flask(__name__)

# Read configuration from the container's runtime environment
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure application logging
app.logger.setLevel(
    getattr(logging, LOG_LEVEL, logging.INFO)
)


@app.route("/")
def home():
    return jsonify({
        "message": "CI/CD Production Lab"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
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
    app.logger.info(
        "Starting application: environment=%s, log_level=%s",
        APP_ENV,
        LOG_LEVEL
    )

    app.run(host="0.0.0.0", port=5000)