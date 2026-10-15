"""
NLP Command Parser - Parse natural language commands into structured actions.
Supports English, Bengali, and Chinese.
"""

import re


# Command patterns
PATTERNS = [
    # Transfer
    {
        "action": "transfer",
        "patterns": [
            r"send\s+([\d.]+)\s*eth\s+to\s+(\w+)",
            r"transfer\s+([\d.]+)\s*eth\s+to\s+(\w+)",
            r"pay\s+(\w+)\s+([\d.]+)\s*eth",
            r"([\w]+)\s*ke\s*([\d.]+)\s*eth\s*(?:pathao|send|de)",
        ],
        "groups": ["amount", "recipient"]
    },
    # Balance check
    {
        "action": "check_balance",
        "patterns": [
            r"(?:what(?:'s| is) my )?balance",
            r"how much (?:eth|money) do i have",
            r"amar\s*balance\s*(?:koto|ki)",
            r"余额",
        ],
        "groups": []
    },
    # Daily report
    {
        "action": "daily_report",
        "patterns": [
            r"daily\s*report",
            r"(?:show|give|get)\s+(?:me\s+)?(?:the\s+)?daily report",
            r"today(?:'s)? (?:expenses|spending|report)",
            r"ajker\s*hisab",
            r"hisab\s*dao",
        ],
        "groups": []
    },
    # Budget status
    {
        "action": "budget_status",
        "patterns": [
            r"^budget$",
            r"(?:show|get)\s+(?:my\s+)?budget",
            r"budget status",
            r"budget\s*dekhao",
        ],
        "groups": []
    },
    # Forecast
    {
        "action": "forecast",
        "patterns": [
            r"(?:show|get)\s+(?:my\s+)?forecast",
            r"predict (?:my )?(?:spending|expenses)",
            r"forecast\s*dekhao",
        ],
        "groups": []
    },
    # Advice
    {
        "action": "advice",
        "patterns": [
            r"should i (?:buy|spend|invest)\s+([\d.]+)\s*eth",
            r"advice on\s+([\d.]+)\s*eth",
            r"([\d.]+)\s*eth\s*(?:kine|invest)\s*korbo",
        ],
        "groups": ["amount"]
    },
    # Swap
    {
        "action": "swap",
        "patterns": [
            r"swap\s+([\d.]+)\s*(\w+)\s+(?:to|for)\s+(\w+)",
            r"convert\s+([\d.]+)\s*(\w+)\s+(?:to|for)\s+(\w+)",
            r"([\d.]+)\s*(\w+)\s*(?:ke|to)\s*(\w+)\s*(?:koro|swap)",
        ],
        "groups": ["amount", "from_token", "to_token"]
    },
    # Currency conversion
    {
        "action": "convert_currency",
        "patterns": [
            r"convert\s+([\d.]+)\s*(\w+)\s+(?:to|into)\s+(\w+)",
            r"([\d.]+)\s*(\w+)\s+(?:to|into)\s+(\w+)\s+convert",
            r"([\d.]+)\s*(\w+)\s*(?:ke|to)\s*(\w+)\s*(?:koro|convert)",
        ],
        "groups": ["amount", "from_currency", "to_currency"]
    },
    # Bill payment with currency conversion
    {
        "action": "pay_bill_converted",
        "patterns": [
            r"pay\s+([\d.]+)\s*(\w+)\s+bill",
            r"([\d.]+)\s*(\w+)\s*bill\s*(?:dite|pay)",
            r"([\d.]+)\s*(\w+)\s*(?:bill|payment)\s*(?:dao|pay|koro)",
        ],
        "groups": ["amount", "currency"]
    },
    # Wallet creation
    {
        "action": "create_wallet",
        "patterns": [
            r"create\s+(?:a\s+)?(?:new\s+)?wallet",
            r"new\s+wallet",
            r"wallet\s*(?:banao|create)",
        ],
        "groups": []
    },
    # Deposit
    {
        "action": "deposit",
        "patterns": [
            r"deposit\s+([\d.]+)\s*(\w+)",
            r"add\s+([\d.]+)\s*(\w+)",
            r"([\d.]+)\s*(\w+)\s*(?:add|deposit)\s*koro",
        ],
        "groups": ["amount", "currency"]
    },
    # Withdraw
    {
        "action": "withdraw",
        "patterns": [
            r"withdraw\s+([\d.]+)\s*(\w+)",
            r"send\s+([\d.]+)\s*(\w+)\s+to\s+my\s+wallet",
            r"([\d.]+)\s*(\w+)\s*(?:withdraw|tolo)",
        ],
        "groups": ["amount", "currency"]
    },
    # Show address / QR
    {
        "action": "show_address",
        "patterns": [
            r"(?:show|get)\s+(?:my\s+)?address",
            r"wallet\s+address",
            r"qr\s*code",
            r"address\s*dekhao",
        ],
        "groups": []
    },
    # Gas estimation
    {
        "action": "estimate_gas",
        "patterns": [
            r"(?:estimate|calculate)\s+gas",
            r"gas\s+fee",
            r"gas\s*koto",
        ],
        "groups": []
    },
    # Multi-chain
    {
        "action": "list_chains",
        "patterns": [
            r"(?:show|list)\s+chains",
            r"supported\s+chains",
            r"ki ki chain",
        ],
        "groups": []
    },
    # Help
    {
        "action": "help",
        "patterns": [
            r"^help$",
            r"what can you do",
            r"ki ki korte paro",
            r"ki korte paro",
            r"commands",
        ],
        "groups": []
    },
]


# Bengali transfer pattern (recipient first)
BENGALI_TRANSFER_PATTERN = r"([\w]+)\s*ke\s*([\d.]+)\s*eth\s*(?:pathao|send|de)"


# Contacts
CONTACTS = {}


def register_contact(name, address):
    CONTACTS[name.lower()] = address
    print(f"[NLP] Registered contact: {name} -> {address[:10]}...")


def resolve_recipient(name):
    if name.startswith("0x") and len(name) == 42:
        return name
    return CONTACTS.get(name.lower())


def parse_command(text):
    text = text.strip().lower()
    
    # Bengali transfer
    bengali_match = re.search(BENGALI_TRANSFER_PATTERN, text)
    if bengali_match:
        recipient_name = bengali_match.group(1)
        amount = bengali_match.group(2)
        try:
            amount = float(amount)
        except ValueError:
            pass
        
        resolved = resolve_recipient(recipient_name)
        params = {
            "amount": amount,
            "recipient": recipient_name,
            "recipient_address": resolved
        }
        if not resolved:
            params["error"] = f"Unknown recipient: {recipient_name}"
        
        return {"action": "transfer", "params": params, "raw": text}
    
    # General patterns
    for pattern_set in PATTERNS:
        for pattern in pattern_set["patterns"]:
            match = re.search(pattern, text)
            if match:
                params = {}
                for i, group_name in enumerate(pattern_set["groups"]):
                    if i < len(match.groups()):
                        value = match.group(i + 1)
                        if group_name == "amount":
                            try:
                                value = float(value)
                            except ValueError:
                                pass
                        params[group_name] = value
                
                if "recipient" in params:
                    resolved = resolve_recipient(params["recipient"])
                    if resolved:
                        params["recipient_address"] = resolved
                    else:
                        params["recipient_address"] = None
                        params["error"] = f"Unknown recipient: {params['recipient']}"
                
                return {
                    "action": pattern_set["action"],
                    "params": params,
                    "raw": text
                }
    
    return {
        "action": "unknown",
        "params": {},
        "raw": text,
        "error": "Could not understand command"
    }


def print_help():
    print("\n[NLP] Available commands:")
    print("  - 'send 0.01 ETH to <name>' - Transfer ETH")
    print("  - '<name> ke 0.01 ETH pathao' - Bengali transfer")
    print("  - 'balance' - Check balance")
    print("  - 'daily report' - Today's expenses")
    print("  - 'budget' - Show budget")
    print("  - 'forecast' - Predict spending")
    print("  - 'should i buy 0.05 ETH' - Get advice")
    print("  - 'swap 0.01 ETH to USDC' - Swap tokens")
    print("  - 'create wallet' - Create new wallet")
    print("  - 'deposit 100 USD' - Deposit fiat")
    print("  - 'withdraw 0.01 ETH' - Withdraw")
    print("  - 'show my address' - Show wallet address + QR")
    print("  - 'estimate gas' - Estimate gas fee")
    print("  - 'list chains' - Show supported chains")
    print("  - 'help' - Show this message")