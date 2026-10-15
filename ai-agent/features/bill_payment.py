"""
Bill Payment module - Schedule and execute recurring bills.
"""

from datetime import datetime


class BillScheduler:
    def __init__(self):
        self.bills = []
    
    def add_bill(self, name, recipient, amount_eth, day_of_month):
        """Add a recurring bill."""
        self.bills.append({
            "name": name,
            "recipient": recipient,
            "amount_eth": amount_eth,
            "day_of_month": day_of_month
        })
        print(f"[BillScheduler] Added: {name} - {amount_eth} ETH on day {day_of_month}")
    
    def get_due_bills(self, today=None):
        """Get bills due today."""
        if today is None:
            today = datetime.now().day
        
        due = [b for b in self.bills if b["day_of_month"] == today]
        return due
    
    def get_upcoming_bills(self, days=7):
        """Get bills due in the next N days."""
        today = datetime.now().day
        upcoming = []
        for bill in self.bills:
            delta = (bill["day_of_month"] - today) % 30
            if 0 <= delta <= days:
                upcoming.append({**bill, "days_until": delta})
        return upcoming
    
    def pay_bill(self, bill, execute_func):
        """Pay a bill via the transaction executor."""
        print(f"\n[BillScheduler] Paying bill: {bill['name']}")
        print(f"  Amount: {bill['amount_eth']} ETH")
        print(f"  Recipient: {bill['recipient'][:10]}...")
        
        result = execute_func(
            bill["recipient"],
            bill["amount_eth"],
            f"Pay {bill['name']} bill"
        )
        
        if result:
            print(f"  PAID: {bill['name']} (tx: {result[:10]}...)")
            return True
        else:
            print(f"  FAILED: {bill['name']}")
            return False


_scheduler = None


def get_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = BillScheduler()
    return _scheduler
