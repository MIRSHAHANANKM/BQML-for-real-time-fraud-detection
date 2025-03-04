import json
import os
import logging
from dotenv import load_dotenv
from web3 import Web3, exceptions

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

if not INFURA_URL or not PRIVATE_KEY or not CONTRACT_ADDRESS:
    logging.error("❌ Missing environment variables! Ensure INFURA_URL, PRIVATE_KEY, and CONTRACT_ADDRESS are set.")
    exit(1)

# Initialize Web3
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not web3.is_connected():
    logging.error("❌ Failed to connect to the Ethereum network. Check INFURA_URL.")
    exit(1)

# Set default account
account = web3.eth.account.from_key(PRIVATE_KEY)
web3.eth.default_account = account.address

logging.info(f"✅ Connected to Ethereum network. Default account: {web3.eth.default_account}")

# Load contract ABI dynamically
contract_abi_path = os.path.join(os.path.dirname(__file__), "contracts/build/FraudDetection.json")

try:
    with open(contract_abi_path, "r") as f:
        contract_json = json.load(f)
        contract_abi = contract_json["abi"]
except FileNotFoundError:
    logging.error(f"❌ Contract ABI file not found: {contract_abi_path}")
    exit(1)

# Load contract instance
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)


def check_balance():
    """Check if the account has enough ETH for transactions."""
    balance = web3.eth.get_balance(web3.eth.default_account)
    eth_balance = web3.from_wei(balance, "ether")
    
    if eth_balance < 0.01:  # Minimum suggested balance
        logging.warning(f"⚠️ Low balance: {eth_balance} ETH. Transactions may fail.")
    
    return balance


def report_fraud(details):
    """Reports a fraud case to the blockchain."""
    try:
        check_balance()

        logging.info(f"🔍 Reporting fraud case: {details}")
        tx = contract.functions.reportFraud(details).build_transaction({
            "from": web3.eth.default_account,
            "gas": 500000,
            "gasPrice": web3.eth.gas_price,  # Dynamic gas price
            "nonce": web3.eth.get_transaction_count(web3.eth.default_account)
        })

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        logging.info(f"✅ Fraud reported successfully! Transaction Hash: {web3.to_hex(tx_hash)}")
        return web3.to_hex(tx_hash)
    
    except exceptions.ContractLogicError as e:
        logging.error(f"🚨 Contract logic error: {e}")
    except ValueError as e:
        logging.error(f"🚨 Transaction error: {e}")
    except Exception as e:
        logging.error(f"❌ Failed to report fraud: {e}")

