
"""
Self-Correction module - AI learns from rejections and adjusts strategy.
"""

from features.accounting import log_decision


def attempt_with_correction(execute_func, to, amount_eth, user_input="", max_attempts=3):
    """Try to execute a transaction. If rejected, adjust and retry."""
    attempts = []
    current_amount = amount_eth
    
    for attempt_num in range(1, max_attempts + 1):
        print(f"\n[Attempt {attempt_num}] Trying {current_amount} ETH...")
        
        result = execute_func(to, current_amount, user_input)
        
        if result is not None:
            attempts.append({
                "attempt": attempt_num,
                "amount": current_amount,
                "result": "SUCCESS",
                "tx_hash": result
            })
            print(f"[Attempt {attempt_num}] SUCCESS with {current_amount} ETH")
            return True, current_amount, result, attempts
        
        reason = get_last_rejection_reason()
        attempts.append({
            "attempt": attempt_num,
            "amount": current_amount,
            "result": "REJECTED",
            "reason": reason
        })
        
        print(f"[Attempt {attempt_num}] REJECTED: {reason}")
        
        new_amount = adjust_amount(current_amount, reason)
        
        if new_amount is None or new_amount == current_amount:
            print(f"Cannot adjust further. Giving up.")
            break
        
        print(f"Adjusting: {current_amount} -> {new_amount} ETH")
        current_amount = new_amount
    
    log_decision(user_input, {"original_amount": amount_eth}, "ALL_ATTEMPTS_FAILED", "GAVE_UP")
    return False, current_amount, None, attempts


def adjust_amount(current_amount, reason):
    """Adjust the transaction amount based on rejection reason."""
    # Check for limit-related reasons (both from verifier and contract)
    if "WITHIN_LIMIT" in reason or "EXCEEDS_PER_TX" in reason:
        # Reduce to 0.009 ETH (safe under 0.01 limit)
        return 0.009
    
    if "EXCEEDS_DAILY" in reason:
        return None
    
    if "EXCEEDS_SESSION" in reason:
        return None
    
    if "NOT_WHITELISTED" in reason or "WHITELISTED" in reason:
        return None
    
    if "ADDRESS_VALID" in reason:
        return None
    
    # Unknown reason - reduce by half
    return current_amount * 0.5


_last_rejection_reason = ""


def set_last_rejection_reason(reason):
    global _last_rejection_reason
    _last_rejection_reason = reason


def get_last_rejection_reason():
    return _last_rejection_reason