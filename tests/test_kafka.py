# test_producer.py
from confluent_kafka import Producer
import json
import time

p = Producer({'bootstrap.servers': 'localhost:9092'})

for i in range(5):
    transaction = {
        "transaction_id": f"TXN_{i+1}",
        "user_id": f"USER_{i+1}",
        "location": "Mumbai",
        "amount": 1000 + i * 500,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    p.produce('fraud_transactions', value=json.dumps(transaction))
    p.flush()
    print(f"Sent: {transaction}")
    time.sleep(2)

