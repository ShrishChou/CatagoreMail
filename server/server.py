from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/train", methods=["GET", "POST"])
def train():
    if request.method == "POST":
        emails = request.json.get('emails', [])
        # Process the emails here
        # For now, we'll just return the count of emails received
        print(emails)
        return jsonify({
            "message": f"Received {len(emails)} emails for training",
            "emailCount": len(emails)
        })
    else:
        return jsonify({
            "message": str(request.method)
        })

if __name__ == "__main__":
    app.run(debug=True, port=8080)