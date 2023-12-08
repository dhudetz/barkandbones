from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
from threading import Lock
from twilio.rest import Client

app = Flask(__name__)
CORS(app)

# Initialize a lock
processing_lock = Lock()
confirm_lock = Lock()
deny_lock = Lock()

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
auth_token = get_api_key(api_key_path)
print(auth_token)
account_sid = 'ACcb8aab937cd40cdb342c3e8246b96b35'
client = Client(account_sid, auth_token)

app = Flask(__name__)
CORS(app)

@app.route('/api/order-deny', methods=['POST'])
def deny_order():
    with confirm_lock:
        order_data = request.get_json()
        process_order(order_data)
        return jsonify({"message": "Order received successfully"}), 200

@app.route('/api/order-confirm', methods=['POST'])
def confirm_order():
    with deny_lock:
        order_data = request.get_json()
        process_order(order_data)
        return jsonify({"message": "Order received successfully"}), 200

@app.route('/api/order', methods=['POST'])
def receive_order():
    with processing_lock:
        order_data = request.get_json()
        process_order(order_data)
        return jsonify({"message": "Order received successfully"}), 200

def process_order(order_data):
    text_message = generate_order_message(order_data)
    phone_number = '+17084463055'
    send_info_text(text_message, phone_number)

def send_info_text(message, number):
    client.messages.create(
        from_ = '+18552044131',
        body = message,
        to = number
    )

def generate_order_message(order_data):
    # Group items by name and count the quantities
    item_counts = {}
    total_cost = 0
    for item in order_data['orderItems']:
        if item['name'] not in item_counts:
            item_counts[item['name']] = 0
        item_counts[item['name']] += 1
        total_cost += item['price']

    # Construct the items string
    items_string = "\n".join(f"{count}x {name}" for name, count in item_counts.items())

    # Construct the message
    message = (
    "NEW ORDER!\n\n"
        f"{order_data['customerName']}\n"
        f"{order_data['phoneNumber']}\n"
        f"{order_data['email']}\n\n"
        f"{items_string}\n\n"
        f"Total: ${total_cost:.2f}\n\n"
        f"Message: {order_data['specialInstructions']}\n\n"
        "<hyperlink>Accept Order\n\n"
        "<hyperlink>Reject Order"
    )

    # For demonstration purposes, we just print the message
    print(message)

    # Return the message in case you need it as a return value
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)