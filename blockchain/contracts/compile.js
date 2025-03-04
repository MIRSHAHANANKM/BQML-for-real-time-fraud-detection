import path from "path";
import fs from "fs-extra";
import solc from "solc";
import { fileURLToPath } from "url";

// Fix __dirname issue in ES Modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Path to the Solidity contract
const contractPath = path.resolve(__dirname, "FraudDetection.sol");

// Read the Solidity file
const source = fs.readFileSync(contractPath, "utf8");

// Solidity compiler input format
const input = {
  language: "Solidity",
  sources: {
    "FraudDetection.sol": {
      content: source,
    },
  },
  settings: {
    outputSelection: {
      "*": {
        "*": ["abi", "evm.bytecode.object"],
      },
    },
  },
};

// Compile the contract
const output = JSON.parse(solc.compile(JSON.stringify(input)));

// Ensure the build directory exists
const buildPath = path.resolve(__dirname, "build");
fs.ensureDirSync(buildPath);

// Extract and save contract JSON
const contractName = "FraudDetection"; // Ensure this matches your contract name!
fs.writeFileSync(
  path.resolve(buildPath, `${contractName}.json`),
  JSON.stringify(output.contracts["FraudDetection.sol"][contractName], null, 2)
);

console.log("✅ Contract compiled successfully! JSON file saved.");
