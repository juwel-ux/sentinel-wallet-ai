"""
Compliance module - Enforce regulatory requirements as code.
"""

import json
import os
from datetime import datetime


COMPLIANCE_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "compliance.jsonl")


class ComplianceEngine:
    def __init__(self):
        self.rules = {
            "max_daily_limit": 0.05,
            "kyc_required_above": 0.01,
            "sanctions_check": True,
            "min_age_days": 0,
        }
        self.kyc_verified = set()
        self.sanctioned = set()
    
    def verify_kyc(self, address):
        self.kyc_verified.add(address)
        print(f"[Compliance] KYC verified: {address[:10]}...")
    
    def add_sanctioned(self, address):
        self.sanctioned.add(address)
        print(f"[Compliance] Added to sanctions: {address[:10]}...")
    
    def check(self, to, amount_eth):
        checks = []
        
        # KYC check
        if amount_eth > self.rules["kyc_required_above"]:
            if to not in self.kyc_verified:
                checks.append(("KYC", False, f"KYC required for amounts > {self.rules['kyc_required_above']} ETH"))
            else:
                checks.append(("KYC", True, "Verified"))
        else:
            checks.append(("KYC", True, "Not required"))
        
        # Sanctions check
        if self.rules["sanctions_check"]:
            if to in self.sanctioned:
                checks.append(("SANCTIONS", False, "Address is sanctioned"))
            else:
                checks.append(("SANCTIONS", True, "Not sanctioned"))
        
        # Daily limit check
        if amount_eth > self.rules["max_daily_limit"]:
            checks.append(("DAILY_LIMIT", False, f"Exceeds {self.rules['max_daily_limit']} ETH"))
        else:
            checks.append(("DAILY_LIMIT", True, "OK"))
        
        all_passed = all(c[1] for c in checks)
        
        # Log compliance check
        entry = {
            "timestamp": datetime.now().isoformat(),
            "to": to,
            "amount": amount_eth,
            "checks": [{"name": c[0], "passed": c[1], "details": c[2]} for c in checks],
            "passed": all_passed
        }
        os.makedirs(os.path.dirname(COMPLIANCE_FILE), exist_ok=True)
        with open(COMPLIANCE_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        return all_passed, checks


_engine = None


def get_compliance():
    global _engine
    if _engine is None:
        _engine = ComplianceEngine()
    return _engine


def check_compliance(to, amount_eth):
    engine = get_compliance()
    return engine.check(to, amount_eth)
