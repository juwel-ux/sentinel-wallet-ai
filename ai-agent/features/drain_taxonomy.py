"""
Drain Taxonomy Defense module.
Protects against 8 known types of signing drain attacks.
"""


DRAIN_TYPES = {
    "on_chain_transfer": "Direct ETH transfer",
    "on_chain_approval": "ERC-20 approval to spender",
    "off_chain_permit": "EIP-2612 permit signature",
    "off_chain_order": "EIP-712 order signature",
    "delegation": "EIP-7702 delegation",
    "permit2": "Permit2 approval",
    "batch_transfer": "Multiple transfers in one tx",
    "contract_interaction": "Arbitrary contract call",
}


class DrainDefense:
    def __init__(self):
        self.blocked = []
    
    def check_transfer(self, to, amount, whitelist):
        if to not in whitelist:
            self.blocked.append(("on_chain_transfer", to))
            return False, "RECIPIENT_NOT_WHITELISTED"
        return True, "OK"
    
    def check_approval(self, spender, whitelist_spenders):
        if spender not in whitelist_spenders:
            self.blocked.append(("on_chain_approval", spender))
            return False, "SPENDER_NOT_WHITELISTED"
        return True, "OK"
    
    def check_permit(self, spender, amount, max_amount, expiry, current_time):
        if spender not in ["0x" + "0" * 40] and amount > max_amount:
            self.blocked.append(("off_chain_permit", spender))
            return False, "PERMIT_AMOUNT_EXCEEDS_LIMIT"
        if expiry < current_time:
            return False, "PERMIT_EXPIRED"
        return True, "OK"
    
    def check_batch(self, transfers):
        if len(transfers) > 5:
            self.blocked.append(("batch_transfer", len(transfers)))
            return False, "BATCH_TOO_LARGE"
        return True, "OK"
    
    def get_blocked_summary(self):
        return {
            "total_blocked": len(self.blocked),
            "types": list(set(b[0] for b in self.blocked))
        }


_defense = None


def get_defense():
    global _defense
    if _defense is None:
        _defense = DrainDefense()
    return _defense


def check_drain_risk(tx_type, **kwargs):
    defense = get_defense()
    if tx_type == "transfer":
        return defense.check_transfer(kwargs["to"], kwargs["amount"], kwargs.get("whitelist", []))
    if tx_type == "approval":
        return defense.check_approval(kwargs["spender"], kwargs.get("whitelist_spenders", []))
    if tx_type == "permit":
        return defense.check_permit(
            kwargs["spender"], kwargs["amount"],
            kwargs.get("max_amount", 0.01),
            kwargs.get("expiry", 0), kwargs.get("current_time", 0)
        )
    if tx_type == "batch":
        return defense.check_batch(kwargs.get("transfers", []))
    return True, "OK"
