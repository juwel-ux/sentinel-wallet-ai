"""
Audit Trail module - Create tamper-proof hash chain of all decisions.
"""

import hashlib
import json
import os
from datetime import datetime


AUDIT_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "audit_chain.jsonl")


def compute_hash(prev_hash, entry_data):
    """Compute hash of (prev_hash + entry_data)."""
    data = prev_hash + json.dumps(entry_data, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()


def get_last_hash():
    """Get the last hash in the chain."""
    if not os.path.exists(AUDIT_FILE):
        return "0" * 64
    
    last = "0" * 64
    with open(AUDIT_FILE) as f:
        for line in f:
            entry = json.loads(line)
            last = entry["hash"]
    return last


def add_audit_entry(action, details):
    """Append an entry to the audit chain."""
    prev_hash = get_last_hash()
    
    entry_data = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details,
        "prev_hash": prev_hash
    }
    
    entry_hash = compute_hash(prev_hash, entry_data)
    entry_data["hash"] = entry_hash
    
    os.makedirs(os.path.dirname(AUDIT_FILE), exist_ok=True)
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry_data) + "\n")
    
    print(f"[AuditTrail] {action} -> hash: {entry_hash[:16]}...")
    return entry_hash


def verify_chain():
    """Verify that the audit chain is intact."""
    if not os.path.exists(AUDIT_FILE):
        return True, "Empty chain"
    
    prev_hash = "0" * 64
    count = 0
    
    with open(AUDIT_FILE) as f:
        for line in f:
            entry = json.loads(line)
            stored_hash = entry.pop("hash")
            
            expected = compute_hash(prev_hash, entry)
            
            if expected != stored_hash:
                return False, f"Chain broken at entry {count}"
            
            prev_hash = stored_hash
            count += 1
    
    return True, f"Chain intact ({count} entries)"


def print_chain():
    """Print the full audit chain."""
    if not os.path.exists(AUDIT_FILE):
        print("[AuditTrail] No entries")
        return
    
    print("\n[AuditTrail] Full chain:")
    with open(AUDIT_FILE) as f:
        for i, line in enumerate(f):
            entry = json.loads(line)
            print(f"  [{i}] {entry['timestamp']} | {entry['action']} | hash: {entry['hash'][:16]}...")
