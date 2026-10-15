"""
Multilingual Response Generator - Generate responses in user's language.
"""


RESPONSES = {
    "transfer_success": {
        "en": "Successfully sent {amount} ETH to {recipient}. TX: {tx}",
        "bn": "{amount} ETH সফলভাবে {recipient}-কে পাঠানো হয়েছে। TX: {tx}",
        "zh": "成功向 {recipient} 发送 {amount} ETH。交易哈希: {tx}",
    },
    "transfer_rejected": {
        "en": "Transaction rejected: {reason}",
        "bn": "লেনদেন প্রত্যাখ্যাত: {reason}",
        "zh": "交易被拒绝: {reason}",
    },
    "balance": {
        "en": "Your balance is {balance} ETH",
        "bn": "আপনার ব্যালেন্স {balance} ETH",
        "zh": "您的余额为 {balance} ETH",
    },
    "daily_report": {
        "en": "Today's report: {count} transactions, total {total} ETH",
        "bn": "আজকের রিপোর্ট: {count}টি লেনদেন, মোট {total} ETH",
        "zh": "今日报告: {count} 笔交易，总计 {total} ETH",
    },
    "budget": {
        "en": "Monthly income: {income} ETH, allocated: {allocated} ETH",
        "bn": "মাসিক আয়: {income} ETH, বরাদ্দ: {allocated} ETH",
        "zh": "月收入: {income} ETH，已分配: {allocated} ETH",
    },
    "advice_safe": {
        "en": "This purchase is safe. Remaining: {remaining} ETH",
        "bn": "এই ক্রয় নিরাপদ। অবশিষ্ট: {remaining} ETH",
        "zh": "此购买是安全的。剩余: {remaining} ETH",
    },
    "advice_risky": {
        "en": "Warning: This purchase is risky. You need {shortfall} ETH more",
        "bn": "সতর্কতা: এই ক্রয় ঝুঁকিপূর্ণ। আপনার আরও {shortfall} ETH প্রয়োজন",
        "zh": "警告: 此购买有风险。您还需要 {shortfall} ETH",
    },
    "unknown": {
        "en": "I didn't understand. Please try again.",
        "bn": "আমি বুঝতে পারিনি। আবার চেষ্টা করুন।",
        "zh": "我不明白。请再试一次。",
    },
    "help": {
        "en": "Available commands: send, balance, report, budget, forecast, advice, swap, help",
        "bn": "উপলব্ধ কমান্ড: send, balance, report, budget, forecast, advice, swap, help",
        "zh": "可用命令: send, balance, report, budget, forecast, advice, swap, help",
    },
}


def get_response(key, lang="en", **kwargs):
    """Get a response in the specified language."""
    if key not in RESPONSES:
        key = "unknown"
    
    template = RESPONSES[key].get(lang, RESPONSES[key]["en"])
    
    try:
        return template.format(**kwargs)
    except KeyError:
        return template


def generate_response_for_command(action, params, lang="en", **context):
    """Generate a response based on the action and language."""
    if action == "transfer":
        if context.get("success"):
            return get_response(
                "transfer_success", lang,
                amount=params.get("amount"),
                recipient=params.get("recipient"),
                tx=context.get("tx", "")[:10]
            )
        else:
            return get_response(
                "transfer_rejected", lang,
                reason=context.get("reason", "Unknown")
            )
    
    if action == "check_balance":
        return get_response("balance", lang, balance=context.get("balance", 0))
    
    if action == "daily_report":
        return get_response(
            "daily_report", lang,
            count=context.get("count", 0),
            total=context.get("total", 0)
        )
    
    if action == "budget_status":
        return get_response(
            "budget", lang,
            income=context.get("income", 0),
            allocated=context.get("allocated", 0)
        )
    
    if action == "advice":
        if context.get("safe"):
            return get_response("advice_safe", lang, remaining=context.get("remaining", 0))
        else:
            return get_response("advice_risky", lang, shortfall=context.get("shortfall", 0))
    
    if action == "help":
        return get_response("help", lang)
    
    return get_response("unknown", lang)
