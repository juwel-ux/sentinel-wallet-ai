"""
Gas Estimator - Estimate transaction fees.
"""

from features.currency_converter import convert


def estimate_gas(w3, contract, agent_address, to, amount_eth):
    """Estimate gas for a transaction."""
    amount_wei = w3.to_wei(amount_eth, "ether")
    
    # Get current gas price
    gas_price_wei = w3.eth.gas_price
    gas_price_gwei = w3.from_wei(gas_price_wei, "gwei")
    
    # Estimate gas
    try:
        gas_estimate = contract.functions.checkAndExecute(to, amount_wei).estimate_gas({
            "from": agent_address
        })
    except Exception as e:
        print(f"[Gas] Estimation failed: {e}")
        return None
    
    # Calculate costs
    total_gas_wei = gas_estimate * gas_price_wei
    total_gas_eth = w3.from_wei(total_gas_wei, "ether")
    
    # Convert to USD
    usd = convert(float(total_gas_eth), "ETH", "USD")
    usd_value = usd["converted"] if usd["success"] else 0
    
    # Convert to BDT
    bdt = convert(float(total_gas_eth), "ETH", "BDT")
    bdt_value = bdt["converted"] if bdt["success"] else 0
    
    print(f"\n[Gas Estimation]")
    print(f"  Gas units: {gas_estimate:,}")
    print(f"  Gas price: {gas_price_gwei:.2f} Gwei")
    print(f"  Total fee: {total_gas_eth:.8f} ETH")
    print(f"  In USD: ${usd_value:.4f}")
    print(f"  In BDT: ৳{bdt_value:.2f}")
    
    return {
        "gas_units": gas_estimate,
        "gas_price_gwei": float(gas_price_gwei),
        "fee_eth": float(total_gas_eth),
        "fee_usd": usd_value,
        "fee_bdt": bdt_value
    }
