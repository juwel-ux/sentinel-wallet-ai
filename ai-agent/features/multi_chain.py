"""
Multi-Chain Support - Ethereum, Polygon, BSC, Sepolia.
"""


CHAINS = {
    "ethereum": {
        "name": "Ethereum Mainnet",
        "rpc": "https://mainnet.infura.io/v3/YOUR_KEY",
        "chain_id": 1,
        "explorer": "https://etherscan.io",
        "native": "ETH",
        "gas_token": "ETH"
    },
    "sepolia": {
        "name": "Sepolia Testnet",
        "rpc": "https://sepolia.infura.io/v3/YOUR_KEY",
        "chain_id": 11155111,
        "explorer": "https://sepolia.etherscan.io",
        "native": "ETH",
        "gas_token": "ETH"
    },
    "polygon": {
        "name": "Polygon Mainnet",
        "rpc": "https://polygon-rpc.com",
        "chain_id": 137,
        "explorer": "https://polygonscan.com",
        "native": "MATIC",
        "gas_token": "MATIC"
    },
    "bsc": {
        "name": "BNB Smart Chain",
        "rpc": "https://bsc-dataseed.binance.org",
        "chain_id": 56,
        "explorer": "https://bscscan.com",
        "native": "BNB",
        "gas_token": "BNB"
    },
    "ganache": {
        "name": "Local Ganache",
        "rpc": "http://127.0.0.1:7545",
        "chain_id": 1337,
        "explorer": "",
        "native": "ETH",
        "gas_token": "ETH"
    }
}


def get_chain(name):
    """Get chain configuration."""
    return CHAINS.get(name.lower())


def list_chains():
    """List all supported chains."""
    print("\n[Supported Chains]")
    for key, chain in CHAINS.items():
        print(f"  {key:12} - {chain['name']} ({chain['native']})")


def get_explorer_url(chain_name, tx_hash):
    """Get explorer URL for a transaction."""
    chain = get_chain(chain_name)
    if not chain or not chain["explorer"]:
        return None
    return f"{chain['explorer']}/tx/{tx_hash}"
