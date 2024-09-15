from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

def get_plain_text_from_html(html_body):
    soup = BeautifulSoup(html_body, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    # Split into lines and remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    # Join non-empty lines
    clean_text = '\n'.join(lines)
    return clean_text.strip()

@app.route("/api/train", methods=["GET", "POST"])
def train():
    if request.method == "POST":
        emails = request.json.get('emails', [])
        #print(emails)
        
        # Initialize empty lists to store the data
        subjects = []
        senders = []
        bodies = []
        read = [] 

        # Read the file and parse each line as JSON
        for json_obj in emails:
            subjects.append(str(json_obj.get('subject', '')))
            senders.append(str(json_obj.get('sender', '')))
            bodies.append(str(json_obj.get('body', '')))
            read.append(str(json_obj.get('read', '')))


        # Create the DataFrame with explicitly defined dtypes
        df = pd.DataFrame({
            'subject': pd.Series(subjects, dtype='string'),
            'sender': pd.Series(senders, dtype='string'),
            'body': pd.Series(bodies, dtype='string'),
            "read": pd.Series(read, dtype='string')
        })

        # Remove rows where 'body' is "No body content"
        df = df[df['body'] != "No body content"]

        # Apply get_plain_text_from_html to the entire 'body' column
        df['body'] = df['body'].apply(get_plain_text_from_html)
        df['body'] = df['body'].astype(str)

        #print(df.head())
        #print(df.tail())
        
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