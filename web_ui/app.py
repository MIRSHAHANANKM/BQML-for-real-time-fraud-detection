from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from confluent_kafka import Consumer, KafkaException
import threading
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Kafka Consumer Configuration
KAFKA_TOPIC = 'fraud_transactions'
KAFKA_BROKER = 'localhost:9092'

consumer_config = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'fraud-monitor-group',
    'auto.offset.reset': 'latest'
}
consumer = Consumer(consumer_config)
consumer.subscribe([KAFKA_TOPIC])

def consume_fraud_data():
    """Consumes real-time fraud data from Kafka and emits updates via SocketIO."""
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                print(f"Kafka Consumer Error: {msg.error()}")
                break
            
            try:
                transaction = json.loads(msg.value().decode('utf-8'))
                socketio.emit('fraud_update', transaction, namespace='/fraud')  # Send data to frontend
                print(f"Sent Fraud Alert: {transaction}")
            except json.JSONDecodeError:
                print("Error decoding JSON message from Kafka")
    except Exception as e:
        print(f"Error in Kafka consumer thread: {e}")
    finally:
        consumer.close()

# Start Kafka Consumer in a Background Thread
thread = threading.Thread(target=consume_fraud_data)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Simple health check for monitoring purposes."""
    return jsonify({"status": "running", "kafka_topic": KAFKA_TOPIC})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5500)
