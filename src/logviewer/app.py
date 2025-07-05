from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logs")
def get_logs():
    logs = []
    try:
        with open(
            "../backend/httpx.jsonl",
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
