from flask import Flask, send_from_directory, jsonify, Response
from typing import Any, Union, Tuple
import json
import os

app = Flask(__name__, static_folder='build/static')


@app.route("/")
def index() -> Response:
    return send_from_directory('build', 'index.html')


@app.route('/<path:path>')
def serve_static_files(path: str) -> Response:
    if os.path.exists(os.path.join('build', path)):
        return send_from_directory('build', path)
    else:
        # For client-side routing, return index.html for unknown routes
        return send_from_directory('build', 'index.html')


@app.route("/logs")
def get_logs() -> Union[Response, Tuple[Response, int]]:
    logs: list[Any] = []
    try:
        with open(
            "../backend/logs/httpx.jsonl",
            "r",
        ) as file:
            for line in file:
                if line.strip():
                    _line = json.loads(line)
                    logs.append(_line)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(logs)


if __name__ == "__main__":
    app.run(debug=True)
