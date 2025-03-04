from confluent_kafka import Producer
import json
import time
import random

# Kafka configuration
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

import random
import time
import json
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_transaction():
    transaction = {
        "transaction_id": random.randint(1000, 9999),
        "amount": round(random.uniform(10, 5000), 2),
        "risk_score": round(random.uniform(0, 1), 2),
        "user_behavior": round(random.uniform(0, 1), 2),
        "device_trust": round(random.uniform(0, 1), 2),
        "signup_time": datetime.utcnow().isoformat(),  # Fix: Add signup_time
        "purchase_time": datetime.utcnow().isoformat(),  # Fix: Add purchase_time
        "device_id": f"device_{random.randint(100, 999)}",
        "source": random.choice(["organic", "ad", "referral"]),
        "browser": random.choice(["Chrome", "Firefox", "Safari", "Edge"]),
        "age": random.randint(18, 70)
    }
    return transaction

while True:
    transaction = generate_transaction()
    producer.send("fraud_transactions", value=transaction)
    print("Sent transaction:", transaction)
    time.sleep(2)  # Simulate real-time transactions
