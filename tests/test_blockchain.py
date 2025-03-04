import unittest
from blockchain.web3_integration import BlockchainIntegration

class TestBlockchain(unittest.TestCase):
    def test_record_fraud(self):
        blockchain_integration = BlockchainIntegration(
            provider_url="http://localhost:8545",
            contract_address="0xYourContractAddress",
            abi_path="blockchain/contracts/FraudDetection.json",
            account="0xYourAccountAddress"
        )
        txn_hash = blockchain_integration.store_fraud_on_blockchain("12345", "Suspicious transaction")
        self.assertTrue(txn_hash.startswith("0x"))

if __name__ == "__main__":
    unittest.main()
