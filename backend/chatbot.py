from flask import Flask, jsonify, Response
from flask_cors import CORS
import openai
import os
import json


app = Flask(__name__)
CORS(app)

def set_backend_directory():
    # Get the current working directory
    current_dir = os.getcwd()

    # Get the name of the last folder in the current path
    folder_name = os.path.basename(current_dir)

    # Check if the current folder is 'barkandbones'
    if folder_name == 'barkandbones':
        # Change directory to './backend'
        new_dir = os.path.join(current_dir, 'backend')
        os.chdir(new_dir)
        print(f"Changed directory to {new_dir}")
    elif folder_name == 'backend':
        print("Already in 'backend' directory")
    else:
        print(f"Current directory is '{folder_name}', not changing directory")

def get_api_key(filepath):
    with open(filepath, 'r') as file:
        return file.readline().strip()

set_backend_directory()
api_key_path = 'api_key.txt'
openai.api_key = get_api_key(api_key_path)

app = Flask(__name__)
CORS(app)

def generate_stream():
    stream = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who runs the Bark and Bones website. The owner is Sarah Hudetz."},
            {"role": "user", "content": "I want to make an order."},
        ],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            message = json.dumps({"message": chunk.choices[0].delta.content})
            yield f"data: {message}\n\n"

@app.route('/api')
def stream_response():
    return Response(generate_stream(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'Connection': 'keep-alive'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)