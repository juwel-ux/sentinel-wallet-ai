"""
Deploy AgentGuard.sol to Ganache using Python only.
Docker-aware: solc is pre-installed in Docker image.
"""

import json
import os
from web3 import Web3
from solcx import compile_standard
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# NOTE: solc is pre-installed in Docker image
# For local development, uncomment the line below:
# from solcx import install_solc
# install_solc("0.8.19")

print("Checking Solidity 0.8.19...")

# Read contract source
contract_path = os.path.join(
    os.path.dirname(__file__), "..", "contracts", "AgentGuard.sol"
)

with open(contract_path, "r") as f:
    contract_source = f.read()

# Compile
print("Compiling...")
compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {"AgentGuard.sol": {"content": contract_source}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "evm.bytecode"]}
            }
        },
    },
    solc_version="0.8.19",
)

contract_data = compiled["contracts"]["AgentGuard.sol"]["AgentGuard"]
abi = contract_data["abi"]
bytecode = contract_data["evm"]["bytecode"]["object"]

# Save ABI
abi_path = os.path.join(
    os.path.dirname(__file__), "..", "ai-agent", "contract_abi.json"
)
with open(abi_path, "w") as f:
    json.dump(abi, f, indent=2)
print(f"ABI saved: {abi_path}")

# Connect to Ganache
GANACHE_URL = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if not w3.is_connected():
    print(f"ERROR: Cannot connect to Ganache at {GANACHE_URL}")
    exit(1)

print(f"Connected to Ganache: {GANACHE_URL}")

# Load accounts
owner = os.getenv("OWNER_ADDRESS")
agent = os.getenv("AGENT_ADDRESS")
recipient = os.getenv("RECIPIENT_ADDRESS")
owner_pk = os.getenv("OWNER_PRIVATE_KEY")

print(f"Owner: {owner}")
print(f"Agent: {agent}")
print(f"Recipient: {recipient}")

# Limits (wei)
PER_TX = w3.to_wei(0.01, "ether")
DAILY = w3.to_wei(0.05, "ether")
SESSION = w3.to_wei(0.05, "ether")

# Deploy
print("\nDeploying...")
AgentGuard = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(owner)

construct_txn = AgentGuard.constructor(
    agent, PER_TX, DAILY, SESSION
).build_transaction({
    "from": owner,
    "nonce": nonce,
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "chainId": 1337,
})

signed = w3.eth.account.sign_transaction(
    construct_txn, private_key=owner_pk
)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print(f"Contract deployed!")
print(f"Contract Address: {contract_address}")

# Add recipient to whitelist
contract = w3.eth.contract(address=contract_address, abi=abi)

nonce = w3.eth.get_transaction_count(owner)
whitelist_txn = contract.functions.addToWhitelist(recipient).build_transaction({
    "from": owner,
    "nonce": nonce,
    "gas": 200000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "chainId": 1337,
})

signed = w3.eth.account.sign_transaction(
    whitelist_txn, private_key=owner_pk
)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Recipient whitelisted: {recipient}")

# Update .env with new contract address
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")

# Read existing .env
with open(env_path, "r") as f:
    lines = f.readlines()

# Remove old CONTRACT_ADDRESS lines
lines = [l for l in lines if not l.startswith("CONTRACT_ADDRESS=")]

# Add new CONTRACT_ADDRESS
lines.append(f"CONTRACT_ADDRESS={contract_address}\n")

# Write back
with open(env_path, "w") as f:
    f.writelines(lines)

print(f"\nDone!")
print(f"CONTRACT_ADDRESS updated in .env")
