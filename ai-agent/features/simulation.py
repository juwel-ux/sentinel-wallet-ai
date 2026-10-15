"""
Simulation module - Dry-run transactions before sending to chain.
"""


class SimulationResult:
    def __init__(self, success, reason="", balance_before=0, balance_after=0, gas_estimate=0):
        self.success = success
        self.reason = reason
        self.balance_before = balance_before
        self.balance_after = balance_after
        self.gas_estimate = gas_estimate

    def __repr__(self):
        return (f"SimulationResult(success={self.success}, "
                f"reason='{self.reason}', "
                f"balance_before={self.balance_before}, "
                f"balance_after={self.balance_after}, "
                f"gas_estimate={self.gas_estimate})")


def simulate_transaction(w3, contract, agent_address, to, amount_eth, gas_price_gwei=20):
    """
    Simulate a transaction using eth_call (no actual state change).
    
    Returns: SimulationResult
    """
    amount_wei = w3.to_wei(amount_eth, "ether")
    
    # Get balances before
    contract_balance_before = w3.eth.get_balance(contract.address)
    recipient_balance_before = w3.eth.get_balance(to)
    
    # Estimate gas
    try:
        gas_estimate = contract.functions.checkAndExecute(to, amount_wei).estimate_gas({
            "from": agent_address
        })
    except Exception as e:
        return SimulationResult(
            success=False,
            reason=f"Gas estimation failed: {str(e)[:100]}",
            balance_before=contract_balance_before
        )
    
    # Check contract balance
    if contract_balance_before < amount_wei:
        return SimulationResult(
            success=False,
            reason=f"Insufficient contract balance: {w3.from_wei(contract_balance_before, 'ether')} ETH < {amount_eth} ETH",
            balance_before=contract_balance_before,
            gas_estimate=gas_estimate
        )
    
    # Simulate (using eth_call, no state change)
    try:
        result = contract.functions.checkAndExecute(to, amount_wei).call({
            "from": agent_address
        })
    except Exception as e:
        return SimulationResult(
            success=False,
            reason=f"Simulation reverted: {str(e)[:100]}",
            balance_before=contract_balance_before,
            gas_estimate=gas_estimate
        )
    
    # Calculate expected balances
    gas_cost = gas_estimate * w3.to_wei(gas_price_gwei, "gwei")
    contract_balance_after = contract_balance_before - amount_wei
    recipient_balance_after = recipient_balance_before + amount_wei
    
    return SimulationResult(
        success=True,
        reason="OK",
        balance_before=contract_balance_before,
        balance_after=contract_balance_after,
        gas_estimate=gas_estimate
    )


def print_simulation(result, to, amount_eth):
    """Print a human-readable simulation report."""
    print(f"\n[Simulation] Dry-run for {amount_eth} ETH -> {to[:10]}...")
    
    if not result.success:
        print(f"[Simulation] FAILED: {result.reason}")
        return False
    
    print(f"[Simulation] PASSED")
    print(f"  Contract balance before: {result.balance_before / 1e18:.6f} ETH")
    print(f"  Contract balance after:  {result.balance_after / 1e18:.6f} ETH")
    print(f"  Gas estimate: {result.gas_estimate}")
    return True
