"""
Anomaly Detection module - Detect unusual spending patterns.
"""

from datetime import datetime, timedelta


class AnomalyDetector:
    def __init__(self, hourly_threshold=5, amount_threshold_multiplier=3.0):
        self.hourly_threshold = hourly_threshold
        self.amount_threshold_multiplier = amount_threshold_multiplier
        self.recent_transactions = []
    
    def record(self, amount_eth, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()
        self.recent_transactions.append({
            "amount": amount_eth,
            "timestamp": timestamp
        })
    
    def check_frequency(self):
        """Check if too many transactions in the last hour."""
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent = [t for t in self.recent_transactions if t["timestamp"] > one_hour_ago]
        
        if len(recent) > self.hourly_threshold:
            return False, f"ANOMALY: {len(recent)} transactions in last hour (max {self.hourly_threshold})"
        return True, "OK"
    
    def check_amount(self, amount_eth):
        """Check if amount is unusually large."""
        if len(self.recent_transactions) < 3:
            return True, "OK (not enough data)"
        
        avg = sum(t["amount"] for t in self.recent_transactions) / len(self.recent_transactions)
        threshold = avg * self.amount_threshold_multiplier
        
        if amount_eth > threshold:
            return False, f"ANOMALY: {amount_eth} ETH > {threshold:.6f} ETH (avg x{self.amount_threshold_multiplier})"
        return True, "OK"
    
    def check_all(self, amount_eth):
        ok1, msg1 = self.check_frequency()
        if not ok1:
            return False, msg1
        ok2, msg2 = self.check_amount(amount_eth)
        if not ok2:
            return False, msg2
        return True, "OK"


_detector = None


def get_detector():
    global _detector
    if _detector is None:
        _detector = AnomalyDetector()
    return _detector


def check_anomaly(amount_eth):
    detector = get_detector()
    return detector.check_all(amount_eth)


def record_transaction(amount_eth):
    detector = get_detector()
    detector.record(amount_eth)
