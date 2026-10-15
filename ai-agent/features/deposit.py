"""
Deposit module - Handle fiat and crypto deposits.
"""

from features.currency_converter import convert
from features.wallet_manager import load_wallet


def calculate_deposit(amount, from_currency, to_crypto="ETH"):
    """Calculate how much crypto you get for your fiat."""
    result = convert(amount, from_currency, to_crypto)
    
    if not result["success"]:
        print(f"[Deposit] Conversion failed: {result['reason']}")
        return None
    
    print(f"\n[Deposit Quote]")
    print(f"  You pay: {amount} {from_currency}")
    print(f"  You get: {result['converted']:.8f} {to_crypto}")
    print(f"  Rate: 1 {from_currency} = {result['rate']:.8f} {to_crypto}")
    
    # Show in BDT if USD
    if from_currency.upper() == "USD":
        bdt = convert(amount, "USD", "BDT")
        if bdt["success"]:
            print(f"  In BDT: ৳{bdt['converted']:.2f}")
    
    return result


def print_deposit_address(name="agent"):
    """Print the deposit address for a wallet."""
    wallet = load_wallet(name)
    if not wallet:
        print(f"[Deposit] Wallet not found: {name}")
        return None
    
    print(f"\n[Deposit Address: {wallet['name']}]")
    print(f"  Address: {wallet['address']}")
    print(f"  Network: {wallet['network']}")
    print(f"  ⚠️  Only send ETH/ERC-20 tokens to this address")
    print(f"  ⚠️  Sending wrong assets may result in loss")
    
    return wallet["address"]


def show_deposit_options():
    """Show all deposit options."""
    print("\n[Deposit Options]")
    print("  1. Bank Transfer → BDT → ETH")
    print("  2. Credit Card → USD → ETH")
    print("  3. Crypto Transfer → ETH/USDC/DAI")
    print("  4. Exchange → Binance/Coinbase → ETH")
    
    print("\n[Recommended Paths]")
    print("  Bangladesh: bKash → Binance P2P → ETH")
    print("  International: Bank → Coinbase → ETH")
    print("  Fastest: Credit Card → MoonPay → ETH")
