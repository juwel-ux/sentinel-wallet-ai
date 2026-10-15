"""
Swap module - Simulated token swap (educational).
In a real deployment, this would call a DEX contract like Uniswap.
"""


class SwapSimulator:
    def __init__(self):
        self.rates = {
            ("ETH", "USDC"): 3000.0,
            ("USDC", "ETH"): 1.0 / 3000.0,
            ("ETH", "DAI"): 3000.0,
            ("DAI", "ETH"): 1.0 / 3000.0,
            ("USDC", "DAI"): 1.0,
            ("DAI", "USDC"): 1.0,
        }
        self.slippage_pct = 0.5
        self.fee_pct = 0.3
    
    def get_rate(self, from_token, to_token):
        key = (from_token.upper(), to_token.upper())
        return self.rates.get(key)
    
    def simulate_swap(self, from_token, to_token, amount):
        rate = self.get_rate(from_token, to_token)
        if not rate:
            return {
                "success": False,
                "reason": f"No rate for {from_token} -> {to_token}"
            }
        
        gross = amount * rate
        fee = gross * (self.fee_pct / 100)
        slippage = gross * (self.slippage_pct / 100)
        net = gross - fee - slippage
        
        return {
            "success": True,
            "from_token": from_token.upper(),
            "to_token": to_token.upper(),
            "amount_in": amount,
            "gross_output": gross,
            "fee": fee,
            "slippage": slippage,
            "net_output": net,
            "rate": rate,
            "effective_rate": net / amount if amount > 0 else 0
        }
    
    def print_swap(self, result):
        if not result["success"]:
            print(f"[Swap] FAILED: {result['reason']}")
            return False
        
        from_t = result['from_token'].upper()
        to_t = result['to_token'].upper()
        print(f"\n[Swap] {result['amount_in']} {from_t} -> {to_t}")
        print(f"  Rate: 1 {from_t} = {result['rate']} {to_t}")
        print(f"  Gross output: {result['gross_output']:.6f} {to_t}")
        print(f"  Fee ({self.fee_pct}%): {result['fee']:.6f}")
        print(f"  Slippage ({self.slippage_pct}%): {result['slippage']:.6f}")
        print(f"  Net output: {result['net_output']:.6f} {to_t}")
        print(f"  Effective rate: {result['effective_rate']:.6f}")
        return True


_simulator = None


def get_swap_simulator():
    global _simulator
    if _simulator is None:
        _simulator = SwapSimulator()
    return _simulator


def simulate_swap(from_token, to_token, amount):
    sim = get_swap_simulator()
    result = sim.simulate_swap(from_token, to_token, amount)
    sim.print_swap(result)
    return result