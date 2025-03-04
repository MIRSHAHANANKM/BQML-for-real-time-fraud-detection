import json
import logging
import time
import signal
import os
from kafka import KafkaConsumer, errors
from blockchain_utils import report_fraud

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Kafka Configuration (Using Environment Variables)
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "127.0.0.1:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "fraud_alerts")

consumer = None  # Global consumer instance for cleanup


def connect_kafka_consumer():
    """Establishes a connection with Kafka Consumer with retries."""
    while True:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                value_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id="fraud_detection_group"
            )
            logging.info("✅ Successfully connected to Kafka.")
            return consumer
        except errors.NoBrokersAvailable:
            logging.error("❌ No Kafka brokers available. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logging.error(f"⚠️ Unexpected error: {e}")
            time.sleep(5)


def signal_handler(sig, frame):
    """Handles termination signals to properly close Kafka Consumer."""
    global consumer
    logging.info("🛑 Received termination signal. Closing Kafka Consumer...")
    if consumer:
        consumer.close()
    exit(0)


def consume_fraud_alerts():
    """Listens for fraud alerts from Kafka and reports them to blockchain."""
    global consumer
    consumer = connect_kafka_consumer()
    logging.info("📡 Listening for fraud alerts...")

    try:
        for message in consumer:
            try:
                if not message.value:
                    logging.warning("⚠️ Received an empty message. Ignoring...")
                    continue
                
                # Ensure JSON structure is valid
                if not isinstance(message.value, dict) or "transaction" not in message.value:
                    logging.error(f"❌ Invalid message format: {message.value}")
                    continue
                
                fraud_details = message.value["transaction"]
                if fraud_details:
                    tx_hash = report_fraud(fraud_details)
                    logging.info(f"🚨 Fraud Detected! Reported on blockchain. Tx Hash: {tx_hash}")
                else:
                    logging.warning("⚠️ Received an empty fraud transaction.")
            except json.JSONDecodeError:
                logging.error("❌ Failed to decode JSON message.")
            except Exception as e:
                logging.error(f"⚠️ Error processing message: {e}")
    except KeyboardInterrupt:
        logging.info("🔴 Stopping Kafka Consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    consume_fraud_alerts()
