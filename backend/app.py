# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api')
def hello_world():
    return jsonify({"message": "Hello from the backend!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)