"""
Withdraw module - Withdraw from agent wallet to external wallet.
"""

from features.currency_converter import convert


def calculate_withdraw(amount_eth, to_currency="USD"):
    """Calculate how much fiat you get when withdrawing."""
    result = convert(amount_eth, "ETH", to_currency)
    
    if not result["success"]:
        print(f"[Withdraw] Conversion failed")
        return None
    
    print(f"\n[Withdraw Quote]")
    print(f"  You send: {amount_eth} ETH")
    print(f"  You get: {result['converted']:.2f} {to_currency}")
    print(f"  Rate: 1 ETH = {result['rate']:.2f} {to_currency}")
    
    # Gas fee estimate
    gas_fee_eth = 0.0005
    gas_fee_usd = convert(gas_fee_eth, "ETH", "USD")
    if gas_fee_usd["success"]:
        print(f"  Est. gas fee: {gas_fee_eth} ETH (~${gas_fee_usd['converted']:.2f})")
    
    return result


def withdraw_to_external(w3, contract, agent_address, agent_pk, to_address, amount_eth):
    """Withdraw ETH from agent wallet to external address."""
    amount_wei = w3.to_wei(amount_eth, "ether")
    
    # Check balance
    balance = w3.eth.get_balance(agent_address)
    if balance < amount_wei:
        print(f"[Withdraw] Insufficient balance")
        print(f"  Available: {w3.from_wei(balance, 'ether')} ETH")
        print(f"  Requested: {amount_eth} ETH")
        return None
    
    # Build transaction
    nonce = w3.eth.get_transaction_count(agent_address)
    txn = {
        "from": agent_address,
        "to": to_address,
        "value": amount_wei,
        "nonce": nonce,
        "gas": 21000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "chainId": 1337
    }
    
    signed = w3.eth.account.sign_transaction(txn, private_key=agent_pk)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"[Withdraw] Success!")
    print(f"  TX: {receipt.transactionHash.hex()}")
    print(f"  Sent: {amount_eth} ETH")
    print(f"  To: {to_address}")
    
    return receipt.transactionHash.hex()
