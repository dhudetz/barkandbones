from flask import Flask, jsonify
from flask_cors import CORS
import openai



app = Flask(__name__)
CORS(app)

# Make sure to set this environment variable in your production environment
openai.api_key = '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'



@app.route('/api')
def hello_world():
    print('starting query')
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who runs the Bark and Bones website. The owner is Sarah Hudetz."},
            {"role": "user", "content": "I want to make an order."},
        ]
    )
    print('ending query')

    # Extract the text from the response
    message = response.choices[0].message.content
    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
