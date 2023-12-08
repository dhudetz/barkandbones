from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
import os
from threading import Lock
from twilio.rest import Client
from random import randint
import smtplib  # For sending email notifications

app = Flask(__name__)
CORS(app)

# Initialize locks
processing_lock = Lock()
confirm_lock = Lock()
deny_lock = Lock()

# Dictionary to store order numbers and associated email addresses
order_email_dict = {}

def set_backend_directory():
    current_dir = os.getcwd()
    folder_name = os.path.basename(current_dir)
    if folder_name == 'barkandbones':
        os.chdir(os.path.join(current_dir, 'backend'))
    elif folder_name != 'backend':
        print(f"Current directory is '{folder_name}', not changing directory")

def get_api_key(filepath):
    with open(filepath, 'r') as file:
        return file.readline().strip()

set_backend_directory()
api_key_path = 'api_key.txt'
auth_token = get_api_key(api_key_path)
account_sid = 'ACcb8aab937cd40cdb342c3e8246b96b35'
client = Client(account_sid, auth_token)

def send_email(recipient_email, subject, body):
    # Configure your email server and sender email here
    sender_email = "barkandbones.orders"
    password = "j34BaR67L9!"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(sender_email, recipient_email, message)
    server.quit()

@app.route('/api/order-confirm/<order_id>', methods=['GET'])
def confirm_order(order_id):
    with confirm_lock:
        current_app.logger.info(f"Order ID: {order_id}")
        email = order_email_dict.get(order_id)
        current_app.logger.info(f"Email: {email}")
        
        if email:
            send_email(email, "Order Confirmation", f"Your order {order_id} has been confirmed.")
            return jsonify({"message": "Order confirmed"}), 200
        else:
            current_app.logger.error("Order ID not found")
            return jsonify({"error": "Order ID not found"}), 404

@app.route('/api/order-deny/<order_id>', methods=['GET'])
def deny_order(order_id):
    with deny_lock:
        email = order_email_dict.get(order_id)
        if email:
            send_email(email, "Order Denied", f"Your order {order_id} has been denied.")
            return jsonify({"message": "Order denied"}), 200
        else:
            return jsonify({"error": "Order ID not found"}), 404

@app.route('/api/order', methods=['POST'])
def receive_order():
    with processing_lock:
        order_data = request.get_json()
        order_id = process_order(order_data)
        return jsonify({"message": "Order received successfully", "order_id": order_id}), 200

def send_info_text(text_message, phone_number):
    client.messages.create(
        from_ = '+18552044131',
        body = text_message,
        to = phone_number
    )

def generate_order_message(order_data, order_id):
    item_counts = {item['name']: order_data['orderItems'].count(item) for item in order_data['orderItems']}
    total_cost = sum(item['price'] for item in order_data['orderItems'])
    items_string = "\n".join(f"{count}x {name}" for name, count in item_counts.items())
    message = (
        f"NEW ORDER!\n\n{order_data['customerName']}\n{order_data['phoneNumber']}\n{order_data['email']}\n\n"
        f"{items_string}\n\nTotal: ${total_cost:.2f}\n\nMessage: {order_data['specialInstructions']}\n\n"
        f"Confirm Order Link: http://barkandbones.org/api/order-confirm/{order_id}\nDeny Order Link: http://barkandbones.org/api/order-deny/{order_id}\n"
        f"Order Number: {order_id}"
    )
    return message

def process_order(order_data):
    order_id = randint(1000000000, 9999999999)
    order_email_dict[order_id] = order_data['email']
    text_message = generate_order_message(order_data, order_id)
    phone_number = '+17084463055'
    send_info_text(text_message, phone_number)
    return order_id

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
