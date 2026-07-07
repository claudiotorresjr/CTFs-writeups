import json
import os

import yaml
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    if not data or "yaml_input" not in data:
        return jsonify({"error": "Missing yaml_input field"}), 400

    yaml_input = data["yaml_input"]
    if not yaml_input.strip():
        return jsonify({"error": "Empty YAML input"}), 400

    try:
        parsed = yaml.load(yaml_input, Loader=yaml.Loader)
        json_output = json.dumps(parsed, indent=2, default=str)
        return jsonify({"result": json_output})
    except yaml.YAMLError as e:
        return jsonify({"error": f"Invalid YAML: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Conversion error: {e}"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "service": "yaml2json",
        "message": "The requested path was not found on the yaml2json converter.",
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
