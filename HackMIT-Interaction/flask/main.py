from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/train', methods=['POST'])
def train():
    if request.method == "POST": 
        return jsonify({"result": "training"}), 200
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST": 
        return jsonify({"result": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)