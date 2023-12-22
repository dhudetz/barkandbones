from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
import os
from threading import Lock
from twilio.rest import Client
from random import randint
import smtplib  # For sending email notifications
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#####################################
#            VARIABLES              #
#####################################
product_prices = {
    'small-treats': 5.00,
    'large-treats': 5.00,
    'delivery': 5.00
}

# DEBUG SWITCH
debug_no_texting = False;
# Twilio Message Number
twilio_phone_number = '+18552044131'

#####################################
#           SETUP/CONFIG            #
#####################################

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Initialize HTTP Limiter
limiter = Limiter(
    get_remote_address, # IP of user
    app=app,
    default_limits=["2 per minute"]
)

# Initialize locks
processing_lock = Lock()
confirm_lock = Lock()
deny_lock = Lock()

# Dictionary to store order numbers and associated email addresses
order_userdata_dict = {}

# Gaurantees in correct root in dev or prod envs.
def set_backend_directory():
    current_dir = os.getcwd()
    folder_name = os.path.basename(current_dir)
    if folder_name == 'barkandbones':
        os.chdir(os.path.join(current_dir, 'backend'))
    elif folder_name != 'backend':
        print(f"Current directory is '{folder_name}', not changing directory")

def get_file_content(filepath):
    with open(filepath, 'r') as file:
        return file.readline().strip()

set_backend_directory()
api_key_path = 'api_key.txt'
auth_token = get_file_content(api_key_path)
account_sid = 'ACcb8aab937cd40cdb342c3e8246b96b35'
client = Client(account_sid, auth_token)

#####################################
#          API ORDER CONFIRM        #
#####################################
@app.route('/api/cfrm/<order_id>', methods=['GET'])
def confirm_order(order_id):
    with confirm_lock:
        try:
            order_id_int = int(order_id)
            order_data = order_userdata_dict.get(order_id_int)
            if order_data and order_data.get('status') == 'pending':
                order_data['status'] = 'confirmed'
                # Construct the email body with all details
                subject, email_body = generate_email_body(order_data, order_id, "confirmed")
                send_email(order_data['email'], subject, email_body)
                return jsonify({"message": "Order confirmed"}), 200
            elif order_data and order_data.get('status') == 'confirmed':
                return jsonify({"error": f"Order status was already confirmed!"}), 400
            elif order_data and order_data.get('status') == 'denied':
                return jsonify({"error": f"Order status was previously denied. You may want to text your customer: {order_data.get('phoneNumber')}"}), 400
            else:
                return jsonify({"error": "Order ID not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid Order ID"}), 400

@app.route('/api/deny/<order_id>', methods=['GET'])
def deny_order(order_id):
    with deny_lock:
        try:
            order_id_int = int(order_id)
            order_data = order_userdata_dict.get(order_id_int)
            if order_data and order_data.get('status') == 'pending':
                # Construct the email body with all details
                subject, email_body = generate_email_body(order_data, order_id, "denied")
                send_email(order_data['email'], subject, email_body)
                return jsonify({"message": "Order denied"}), 200
            elif order_data and order_data.get('status') == 'denied':
                return jsonify({"error": f"Order status was already denied!"}), 400
            elif order_data and order_data.get('status') == 'confirmed':
                return jsonify({"error": f"Order status was previously confirmed. You may want to text your customer: {order_data.get('phoneNumber')}"}), 400
            else:
                return jsonify({"error": "Order ID not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid Order ID"}), 400

#####################################
#            LOG SYSTEM             #
#####################################

from datetime import datetime

# Log order details
def log_order(order_data, order_id):
    with open('orders.txt', 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order_log = f"{timestamp} - Order ID: {order_id}, Customer Name: {order_data['customerName']}, Total Cost: ${order_data['totalPrice']:.2f}\n"
        file.write(order_log)

# Log general server access
def log_access(endpoint):
    with open('log.txt', 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - Access to endpoint: {endpoint}\n"
        file.write(log_entry)

#####################################
#            PROCESS ORDER          #
#####################################
@app.route('/api/order', methods=['POST'])
def receive_order():
    log_access('/api/order')  # Log server access
    with processing_lock:
        order_data = request.get_json()
        order_id = process_order(order_data)
        
        # Log the new order
        log_order(order_data, order_id)
        
        return jsonify({"message": "Order received successfully", "order_id": order_id}), 200

def process_order(order_data):
    # Calculate the total price on the server side
    total_price = 0
    for item in order_data['orderItems']:
        product_id = item['id']  # Securely use 'id' to get the product price
        quantity = item.get('quantity', 1)  # Default to 1 if quantity not provided
        total_price += product_prices.get(product_id, 0) * quantity

    # Generate an order ID
    order_id = randint(1000000000, 9999999999)

    # Add the total price to order data
    order_data['totalPrice'] = total_price

    # Continue with the rest of your order processing
    order_userdata_dict[order_id] = order_data
    order_userdata_dict[order_id]['status'] = 'pending'

    # Get the text message ready
    text_message = generate_order_text(order_data, order_id)
    message_config_path = 'message_config.txt' # Get the saved phone number
    phone_number = get_file_content(message_config_path)
    send_info_text(text_message, phone_number)

    return order_id

#####################################
#        MESSAGES AND EMAILS        #
#####################################
def send_info_text(text_message, phone_number):
    if debug_no_texting:
        return;
    client.messages.create(
        from_ = twilio_phone_number,
        body = text_message,
        to = phone_number
    )

def send_email(recipient_email, subject, body):
    # Configure your email server and sender email here
    sender_email = "barkandbones.orders@gmail.com"
    password = "ogwp vpet areb uuou"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(sender_email, recipient_email, message)
    server.quit()

def generate_email_body(order_data, order_id, status):
    if status == "confirmed":
        subject = "Order Confirmation"
        body = "Success! Your order has been confirmed!\n\n"
    else:
        subject = "Order Denied"
        body = "Unfortunately, your order has been denied due to our production limitations.\n\n"

    # Count the occurrences of each item
    item_counts = {}
    for item in order_data['orderItems']:
        item_id = item['id']
        if item_id in item_counts:
            item_counts[item_id] += 1
        else:
            item_counts[item_id] = 1

    # Generate item list and calculate total cost
    item_list = "\n".join(f"{count}x {item_id}" for item_id, count in item_counts.items())
    total_cost = sum(product_prices.get(item_id, 0) * count for item_id, count in item_counts.items())

    body += (
        f"Order ID: {order_id}\n"
        f"Customer Name: {order_data['customerName']}\n"
        f"Phone Number: {order_data['phoneNumber']}\n"
        f"Email: {order_data['email']}\n"
        f"Address: {order_data['address']}\n\n"
        f"Items:\n{item_list}\n\n"
        f"Total Cost: ${total_cost:.2f}\n\n"
        f"Thank you for doing business with Bark and Bones."
    )
    return subject, body




def generate_order_text(order_data, order_id):
    item_counts = {item['name']: order_data['orderItems'].count(item) for item in order_data['orderItems']}
    total_cost = sum(item['price'] for item in order_data['orderItems'])
    items_string = "\n".join(f"{count}x {name}" for name, count in item_counts.items())
    message = (
        f"NEW ORDER!\n\n{order_data['customerName']}\n"
        f"{order_data['phoneNumber']}\n"
        f"{order_data['email']}\n"
        f"{order_data['address']}\n\n"
        f"{items_string}\nTotal: ${total_cost:.2f}\n\nMessage: {order_data['specialInstructions']}\n\n"
        f"Confirm Order Link: http://barkandbones.org/api/cfrm/{order_id}\n\nDeny Order Link: http://barkandbones.org/api/deny/{order_id}\n\n"
    )
    return message

#####################################
#      FLASK BACKEND STARTUP        #
#####################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
