"""
Portfolio Monitoring module - Track balances and detect anomalies.
"""


class PortfolioMonitor:
    def __init__(self):
        self.snapshots = []
    
    def take_snapshot(self, w3, addresses):
        """Take a balance snapshot of all addresses."""
        snapshot = {}
        for name, addr in addresses.items():
            balance = w3.eth.get_balance(addr)
            snapshot[name] = w3.from_wei(balance, "ether")
        self.snapshots.append(snapshot)
        return snapshot
    
    def compare_with_previous(self):
        """Compare current snapshot with previous."""
        if len(self.snapshots) < 2:
            return None
        prev = self.snapshots[-2]
        curr = self.snapshots[-1]
        changes = {}
        for name in curr:
            if name in prev:
                changes[name] = float(curr[name]) - float(prev[name])
        return changes
    
    def print_portfolio(self, snapshot):
        print("\n[Portfolio]")
        total = 0
        for name, balance in snapshot.items():
            print(f"  {name}: {balance} ETH")
            total += float(balance)
        print(f"  TOTAL: {total:.6f} ETH")


_monitor = None


def get_monitor():
    global _monitor
    if _monitor is None:
        _monitor = PortfolioMonitor()
    return _monitor


def print_portfolio(w3, addresses):
    monitor = get_monitor()
    snapshot = monitor.take_snapshot(w3, addresses)
    monitor.print_portfolio(snapshot)
    return snapshot
