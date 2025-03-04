import Web3 from "web3";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

// Load Environment Variables
dotenv.config();

// Convert __dirname for ESM compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load Config
const INFURA_URL = process.env.INFURA_URL;
const PRIVATE_KEY = process.env.PRIVATE_KEY;

// Web3 Setup
const web3 = new Web3(new Web3.providers.HttpProvider(INFURA_URL));

// Load Contract ABI and Bytecode
const contractPath = path.resolve(__dirname, "./build/FraudDetection.json");
const contractData = JSON.parse(fs.readFileSync(contractPath, "utf8"));
const { abi, evm } = contractData;

// Account Setup
const account = web3.eth.accounts.privateKeyToAccount(PRIVATE_KEY);
web3.eth.accounts.wallet.add(account);
web3.eth.defaultAccount = account.address;

async function deployContract() {
  try {
    console.log(` Deploying contract from: ${account.address}`);

    // Check Account Balance
    const balance = await web3.eth.getBalance(account.address);
    const balanceInEth = web3.utils.fromWei(balance, "ether");
    console.log(` Account Balance: ${balanceInEth} ETH`);

    if (parseFloat(balanceInEth) < 0.01) {
      throw new Error(" Insufficient funds! Please add more ETH.");
    }

    // Deploy Contract
    const contract = new web3.eth.Contract(abi);
    const gasPrice = await web3.eth.getGasPrice();
    const deployTx = contract.deploy({ data: evm.bytecode.object });

    // Estimate Gas
    const estimatedGas = await deployTx.estimateGas({ from: account.address });
    console.log(` Estimated Gas: ${estimatedGas}`);

    // Send Transaction
    const deployedContract = await deployTx.send({
      from: account.address,
      gas: estimatedGas,
      gasPrice: gasPrice,
    });

    console.log(` Contract deployed at: ${deployedContract.options.address}`);
  } catch (error) {
    console.error("🚨 Deployment Failed:", error.message);
  }
}

// Run Deployment
deployContract();
