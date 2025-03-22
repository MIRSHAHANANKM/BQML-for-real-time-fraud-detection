import unittest
from blockchain.web3_integration import Blockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()

    def test_add_transaction(self):
        tx = {"sender": "Alice", "receiver": "Bob", "amount": 100}
        self.blockchain.add_transaction(tx)
        self.assertIn(tx, self.blockchain.unconfirmed_transactions)

    def test_create_new_block(self):
        initial_length = len(self.blockchain.chain)
        self.blockchain.mine()
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)

    def test_chain_validity(self):
        self.blockchain.mine()
        is_valid = self.blockchain.is_chain_valid(self.blockchain.chain)
        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()

