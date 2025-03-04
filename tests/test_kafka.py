import unittest
from kafka_producer import KafkaProducerClient
from kafka_consumer import KafkaConsumerClient

class TestKafkaIntegration(unittest.TestCase):
    def test_producer_consumer_integration(self):
        producer = KafkaProducerClient()
        message = {"fraud_alert": "test message"}
        producer.send_message(message)
        producer.close()

        consumer = KafkaConsumerClient()
        consumer.listen()  # This should receive and process the above message

if __name__ == "__main__":
    unittest.main()
