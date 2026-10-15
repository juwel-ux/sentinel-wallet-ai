"""
Multi-Agent Verification module.
An independent verifier agent checks every transaction before execution.
"""

from features.accounting import log_decision


class VerifierAgent:
    """
    Independent verifier that checks transactions.
    Has NO connection to the planner's context.
    """
    
    def __init__(self, whitelist=None, max_amount=0.01):
        self.whitelist = whitelist or []
        self.max_amount = max_amount
        self.verification_log = []
    
    def verify(self, to_address, amount_eth, contract_state=None):
        """
        Verify a transaction independently.
        Returns: (approved, reason)
        """
        checks = []
        
        # Check 1: Address validity
        if not to_address or len(to_address) != 42 or not to_address.startswith("0x"):
            checks.append(("ADDRESS_VALID", False, "Invalid address format"))
        else:
            checks.append(("ADDRESS_VALID", True, "OK"))
        
        # Check 2: Address in whitelist
        if to_address not in self.whitelist:
            checks.append(("WHITELISTED", False, "Address not in whitelist"))
        else:
            checks.append(("WHITELISTED", True, "OK"))
        
        # Check 3: Amount is positive
        if amount_eth <= 0:
            checks.append(("AMOUNT_POSITIVE", False, "Amount must be positive"))
        else:
            checks.append(("AMOUNT_POSITIVE", True, "OK"))
        
        # Check 4: Amount within limit
        if amount_eth > self.max_amount:
            checks.append(("WITHIN_LIMIT", False, f"Exceeds {self.max_amount} ETH limit"))
        else:
            checks.append(("WITHIN_LIMIT", True, "OK"))
        
        # Check 5: Amount has max 6 decimals
        if round(amount_eth, 6) != amount_eth:
            checks.append(("DECIMALS_OK", False, "Too many decimals"))
        else:
            checks.append(("DECIMALS_OK", True, "OK"))
        
        # Log verification
        entry = {
            "to": to_address,
            "amount": amount_eth,
            "checks": checks
        }
        self.verification_log.append(entry)
        
        # All checks must pass
        for check_name, passed, reason in checks:
            if not passed:
                print(f"[Verifier] REJECTED at {check_name}: {reason}")
                return False, f"{check_name}: {reason}"
        
        print(f"[Verifier] APPROVED: {amount_eth} ETH -> {to_address[:10]}...")
        return True, "OK"
    
    def get_verification_log(self):
        return self.verification_log


# Singleton verifier
_verifier = None


def get_verifier(whitelist=None, max_amount=0.01):
    global _verifier
    if _verifier is None:
        _verifier = VerifierAgent(whitelist=whitelist, max_amount=max_amount)
    return _verifier


def verify_transaction(to_address, amount_eth, whitelist=None, max_amount=0.01):
    """Convenience function to verify a transaction."""
    verifier = get_verifier(whitelist=whitelist, max_amount=max_amount)
    return verifier.verify(to_address, amount_eth)