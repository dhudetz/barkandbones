# app.py
from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
from random import randint


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

frontend_messages = ["bone", "sarah", "more", "&", "charlie", "bark"]

@app.route('/api')
def hello_world():
    message = frontend_messages[randint(0,len(frontend_messages)-1)]
    return jsonify({"message": message, "data": randint(0,10000)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
