"""
Proof-Gated Signing module.
Generates a proof that a transaction satisfies all policies before signing.
"""

import hashlib
import json
from datetime import datetime


class PolicyProof:
    def __init__(self, tx_data, policy_checks):
        self.tx_data = tx_data
        self.policy_checks = policy_checks
        self.timestamp = datetime.now().isoformat()
        self.proof_hash = self._compute_hash()
    
    def _compute_hash(self):
        data = json.dumps({
            "tx": self.tx_data,
            "checks": self.policy_checks,
            "timestamp": self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()
    
    def is_valid(self):
        return all(check["passed"] for check in self.policy_checks)
    
    def to_dict(self):
        return {
            "tx": self.tx_data,
            "checks": self.policy_checks,
            "timestamp": self.timestamp,
            "proof_hash": self.proof_hash,
            "valid": self.is_valid()
        }


def generate_proof(to, amount_eth, checks):
    """
    Generate a proof that a transaction satisfies policies.
    checks: list of {"name": str, "passed": bool, "details": str}
    """
    tx_data = {"to": to, "amount": amount_eth}
    proof = PolicyProof(tx_data, checks)
    return proof


def print_proof(proof):
    print(f"\n[ProofGated] Policy proof: {proof.proof_hash[:16]}...")
    for check in proof.policy_checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  [{status}] {check['name']}: {check['details']}")
    print(f"  Valid: {proof.is_valid()}")
