import threading
import subprocess

def start_producer():
    """Run Kafka producer in a separate thread"""
    subprocess.run(["python", r"real_time_engine\kafka_producer.py"])

def start_consumer():
    """Run Kafka consumer in a separate thread"""
    subprocess.run(["python", r"real_time_engine\kafka_consumer.py"])

if __name__ == "__main__":
    print("Starting Real-Time Fraud Detection Engine...")

    producer_thread = threading.Thread(target=start_producer)
    consumer_thread = threading.Thread(target=start_consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

