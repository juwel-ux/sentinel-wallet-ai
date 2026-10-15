"""
Currency Converter - Convert between USD, BDT, ETH, and other currencies.
"""


FALLBACK_RATES = {
    "USD_BDT": 117.0,
    "USD_ETH": 0.00033,
    "BDT_ETH": 0.0000028,
    "BDT_USD": 1 / 117.0,
    "ETH_USD": 3000.0,
    "ETH_BDT": 351000.0,
    "CNY_BDT": 16.2,
    "USD_CNY": 7.24,
    "CNY_USD": 1 / 7.24,
    "BDT_CNY": 1 / 16.2,
}


def get_rate(from_currency, to_currency):
    """Get exchange rate between two currencies."""
    from_c = from_currency.upper()
    to_c = to_currency.upper()
    
    if from_c == to_c:
        return 1.0
    
    key = f"{from_c}_{to_c}"
    if key in FALLBACK_RATES:
        return FALLBACK_RATES[key]
    
    reverse_key = f"{to_c}_{from_c}"
    if reverse_key in FALLBACK_RATES:
        return 1.0 / FALLBACK_RATES[reverse_key]
    
    return None


def convert(amount, from_currency, to_currency):
    """Convert amount from one currency to another."""
    rate = get_rate(from_currency, to_currency)
    
    if rate is None:
        return {
            "success": False,
            "reason": f"No rate for {from_currency} -> {to_currency}"
        }
    
    converted = amount * rate
    
    return {
        "success": True,
        "amount": amount,
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "rate": rate,
        "converted": converted
    }


def print_conversion(result):
    """Print conversion result."""
    if not result["success"]:
        print(f"[Currency] FAILED: {result['reason']}")
        return False
    
    print(f"\n[Currency] {result['amount']} {result['from_currency']} -> "
          f"{result['converted']:.4f} {result['to_currency']}")
    print(f"  Rate: 1 {result['from_currency']} = {result['rate']:.6f} {result['to_currency']}")
    return True


def usd_to_bdt(usd):
    return convert(usd, "USD", "BDT")


def bdt_to_usd(bdt):
    return convert(bdt, "BDT", "USD")


def usd_to_eth(usd):
    return convert(usd, "USD", "ETH")


def eth_to_bdt(eth):
    return convert(eth, "ETH", "BDT")


def bdt_to_eth(bdt):
    return convert(bdt, "BDT", "ETH")
