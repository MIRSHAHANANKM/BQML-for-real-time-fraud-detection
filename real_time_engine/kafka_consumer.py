import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from confluent_kafka import Consumer, KafkaError
import json
import torch
from meta_learning.meta_learning_model import FraudMetaModel
from meta_learning.data_preprocessing import scaler

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
    
    # Check for missing keys
    for key in required_keys:
        if key not in transaction:
            print(f"⚠️ Warning: Missing key '{key}' in transaction: {transaction}")
            return False, 0.0  # Default fraud result

    # Preprocess features
    features = torch.tensor(scaler.transform([[ 
        transaction["amount"], transaction["risk_score"], transaction["user_behavior"], 
        transaction["device_trust"], transaction["signup_time"], transaction["purchase_time"],
        transaction["device_id"], transaction["source"], transaction["browser"], transaction["age"]
    ]]), dtype=torch.float32)

    prediction = model(features).item()
    is_fraud = prediction > 0.5
    return is_fraud, prediction


print("Fraud Detection Consumer Started...")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        transaction = msg.value().decode('utf-8')  # Decode message
        print("Received transaction:", transaction) 
        

    transaction = json.loads(msg.value().decode('utf-8'))
    is_fraud, fraud_probability = detect_fraud(transaction)

    print(f"Transaction ID: {transaction['transaction_id']} | Fraud Probability: {fraud_probability:.4f} | Fraudulent: {is_fraud}")

