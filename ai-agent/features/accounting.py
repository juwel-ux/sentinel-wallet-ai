"""
Accounting module - record and report all transactions.
"""

import json
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

TRANSACTIONS_FILE = os.path.join(LOG_DIR, "transactions.jsonl")
REJECTIONS_FILE = os.path.join(LOG_DIR, "rejections.jsonl")
DECISIONS_FILE = os.path.join(LOG_DIR, "decisions.jsonl")


def log_transaction(tx_hash, to_address, amount_eth, status, reason=""):
    """Record a transaction (success or rejection)."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "tx_hash": tx_hash,
        "to": to_address,
        "amount_eth": amount_eth,
        "status": status,
        "reason": reason
    }
    
    if status == "SUCCESS":
        with open(TRANSACTIONS_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    else:
        with open(REJECTIONS_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    print(f"Logged: {status} - {amount_eth} ETH to {to_address[:10]}...")


def log_decision(user_input, plan, check_result, action):
    """Record an AI decision."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "plan": plan,
        "check_result": check_result,
        "action": action
    }
    with open(DECISIONS_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def get_today_transactions():
    """Get all transactions from today."""
    today = datetime.now().strftime("%Y-%m-%d")
    transactions = []
    
    if not os.path.exists(TRANSACTIONS_FILE):
        return transactions
    
    with open(TRANSACTIONS_FILE, "r") as f:
        for line in f:
            entry = json.loads(line)
            if entry["timestamp"].startswith(today):
                transactions.append(entry)
    
    return transactions


def get_today_rejections():
    """Get all rejections from today."""
    today = datetime.now().strftime("%Y-%m-%d")
    rejections = []
    
    if not os.path.exists(REJECTIONS_FILE):
        return rejections
    
    with open(REJECTIONS_FILE, "r") as f:
        for line in f:
            entry = json.loads(line)
            if entry["timestamp"].startswith(today):
                rejections.append(entry)
    
    return rejections


def daily_report():
    """Generate today's summary report."""
    transactions = get_today_transactions()
    rejections = get_today_rejections()
    
    total_sent = sum(tx["amount_eth"] for tx in transactions)
    total_rejected = sum(rj["amount_eth"] for rj in rejections)
    
    print("\n" + "=" * 50)
    print("DAILY ACCOUNTING REPORT")
    print("=" * 50)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"\nSuccessful transactions: {len(transactions)}")
    print(f"Total sent: {total_sent:.6f} ETH")
    
    for tx in transactions:
        print(f"  - {tx['amount_eth']} ETH -> {tx['to'][:10]}... (tx: {tx['tx_hash'][:10]}...)")
    
    print(f"\nRejected transactions: {len(rejections)}")
    print(f"Total rejected amount: {total_rejected:.6f} ETH")
    
    for rj in rejections:
        print(f"  - {rj['amount_eth']} ETH REJECTED: {rj['reason']}")
    
    print("=" * 50)
    
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "successful_count": len(transactions),
        "total_sent": total_sent,
        "rejected_count": len(rejections),
        "total_rejected": total_rejected
    }