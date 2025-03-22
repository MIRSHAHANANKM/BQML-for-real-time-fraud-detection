import sys
import os
import json
import torch
from confluent_kafka import Consumer, KafkaError
from meta_learning.meta_learning_model import FraudMetaModel
from meta_learning.data_preprocessing import scaler

#  Add Flask SocketIO alert emit
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'web_ui'))
from web_ui.app import send_fraud_alert  # Import emit function from Flask-SocketIO app

# Kafka Consumer configuration
conf = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'fraud-detector',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf)
consumer.subscribe(['fraud-transactions'])

# Load trained fraud detection model
model = FraudMetaModel(input_size=10)
model.load_state_dict(torch.load("meta_fraud_model.pth"))
model.eval()

def detect_fraud(transaction):
    """Run fraud detection on a transaction"""
    required_keys = ["amount", "risk_score", "user_behavior", "device_trust",
                     "signup_time", "purchase_time", "device_id", "source",
                     "browser", "age"]

    for key in required_keys:
        if key not in transaction:
            print(f" Warning: Missing key '{key}' in transaction: {transaction}")
            return False, 0.0

    try:
        features = torch.tensor(scaler.transform([[ 
            transaction["amount"], transaction["risk_score"], transaction["user_behavior"], 
            transaction["device_trust"], transaction["signup_time"], transaction["purchase_time"],
            transaction["device_id"], transaction["source"], transaction["browser"], transaction["age"]
        ]]), dtype=torch.float32)

        prediction = model(features).item()
        is_fraud = prediction > 0.5
        return is_fraud, prediction
    except Exception as e:
        print(f" Error during fraud detection: {e}")
        return False, 0.0

print("Fraud Detection Consumer Started...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print(f"Kafka Error: {msg.error()}")
            continue

        transaction = json.loads(msg.value().decode('utf-8'))
        print(f" Received transaction: {transaction}")
        
        is_fraud, fraud_prob = detect_fraud(transaction)

        print(f" Transaction ID: {transaction.get('transaction_id', 'N/A')} | Fraud Probability: {fraud_prob:.4f} | Fraudulent: {is_fraud}")

        #  Emit alert to frontend if fraud detected
        if is_fraud:
            alert = {
                'transaction_id': transaction.get('transaction_id', 'N/A'),
                'user_id': transaction.get('user_id', 'Unknown'),
                'device_id': transaction.get('device_id', 'Unknown'),
                'fraud_probability': round(fraud_prob, 4)
            }
            send_fraud_alert(alert)

except KeyboardInterrupt:
    print(" Consumer Stopped.")
finally:
    consumer.close()
