import unittest
from real_time_engine.fraud_detection_engine import FraudDetectionEngine

class TestFraudDetection(unittest.TestCase):
    def test_fraud_detection(self):
        fraud_engine = FraudDetectionEngine()
        fraud_data = {"transaction_id": "12345", "fraud_details": "Suspicious transaction"}
        fraud_engine.process_fraud_data(fraud_data)

if __name__ == "__main__":
    unittest.main()
