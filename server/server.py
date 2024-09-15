from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/train", methods=["GET"])
def train():
    return jsonify({
        "message": "Hello ffw World"
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)