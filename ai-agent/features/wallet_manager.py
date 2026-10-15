"""
Wallet Manager - Create and manage agent wallets.
"""

import json
import os
from eth_account import Account
from datetime import datetime


WALLET_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "wallets")
os.makedirs(WALLET_DIR, exist_ok=True)


def create_agent_wallet(name="agent", password=""):
    """Create a new agent wallet."""
    Account.enable_unaudited_hdwallet_features()
    
    # Generate new account
    account = Account.create()
    
    wallet = {
        "name": name,
        "address": account.address,
        "private_key": account.key.hex(),
        "created_at": datetime.now().isoformat(),
        "network": "ethereum"
    }
    
    # Save wallet
    filepath = os.path.join(WALLET_DIR, f"{name}.json")
    with open(filepath, "w") as f:
        json.dump(wallet, f, indent=2)
    
    print(f"[Wallet] Created: {name}")
    print(f"  Address: {account.address}")
    print(f"  Private Key: {account.key.hex()[:20]}...")
    print(f"  ⚠️  KEEP PRIVATE KEY SAFE!")
    
    return wallet


def load_wallet(name="agent"):
    """Load an existing wallet."""
    filepath = os.path.join(WALLET_DIR, f"{name}.json")
    if not os.path.exists(filepath):
        return None
    
    with open(filepath) as f:
        return json.load(f)


def list_wallets():
    """List all wallets."""
    wallets = []
    for filename in os.listdir(WALLET_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(WALLET_DIR, filename)
            with open(filepath) as f:
                wallet = json.load(f)
                wallets.append({
                    "name": wallet["name"],
                    "address": wallet["address"],
                    "created_at": wallet["created_at"]
                })
    return wallets


def get_wallet_balance(w3, address):
    """Get ETH balance of a wallet."""
    balance_wei = w3.eth.get_balance(address)
    return w3.from_wei(balance_wei, "ether")


def print_wallet_info(w3, name="agent"):
    """Print wallet information."""
    wallet = load_wallet(name)
    if not wallet:
        print(f"[Wallet] Not found: {name}")
        return
    
    balance = get_wallet_balance(w3, wallet["address"])
    
    print(f"\n[Wallet: {wallet['name']}]")
    print(f"  Address: {wallet['address']}")
    print(f"  Balance: {balance} ETH")
    print(f"  Created: {wallet['created_at']}")
    print(f"  Network: {wallet['network']}")
