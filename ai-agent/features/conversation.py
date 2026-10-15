"""
Conversational AI module - Natural conversation with financial focus.
"""


USER_PROFILE = {
    "name": "Emdad",
    "language": "bn",
    "balance": 99.97,
    "today_spent": 0.018,
    "budget_used": 60,
}


FINANCIAL_KEYWORDS = [
    "balance", "send", "transfer", "pay", "bill", "budget", "spend", "spent",
    "eth", "usd", "bdt", "cny", "swap", "convert", "deposit", "withdraw",
    "wallet", "address", "gas", "transaction", "money", "crypto", "coin",
    "report", "forecast", "advice", "invest", "savings", "income", "expense",
    "price", "cost", "fee", "limit", "account", "blockchain", "token",
    "dollar", "taka", "yuan", "bitcoin", "ethereum", "usdc", "dai",
    "ব্যালেন্স", "পাঠাও", "টাকা", "বিল", "বাজেট", "খরচ", "ইথ", "ডলার",
    "সোয়াপ", "কনভার্ট", "ডিপোজিট", "উইথড্র", "ওয়ালেট", "অ্যাড্রেস",
    "গ্যাস", "লেনদেন", "হিসাব", "পরামর্শ", "বিনিয়োগ", "সঞ্চয়", "আয়",
    "দাম", "ফি", "লিমিট", "অ্যাকাউন্ট", "টোকেন", "ক্রিপ্টো",
    "余额", "发送", "转账", "支付", "账单", "预算", "花费", "以太",
    "美元", "人民币", "交换", "转换", "存款", "提款", "钱包", "地址",
    "燃料", "交易", "报告", "建议", "投资", "储蓄", "收入", "费用",
]


def is_financial_topic(text):
    text = text.lower().strip()
    return any(k in text for k in FINANCIAL_KEYWORDS)


def detect_intent(text):
    text = text.lower().strip()
    if any(g in text for g in ["hello", "hi", "hey", "হ্যালো", "হাই", "নমস্কার", "你好", "嗨"]):
        return "greeting"
    if any(p in text for p in ["how are you", "কেমন আছ", "কেমন আছো", "你好吗"]):
        return "how_are_you"
    if any(p in text for p in ["thank", "thanks", "ধন্যবাদ", "শুকরিয়া", "谢谢"]):
        return "thanks"
    if any(p in text for p in ["bye", "goodbye", "বিদায়", "আলবিদা", "再见"]):
        return "farewell"
    if any(p in text for p in ["balance", "ব্যালেন্স", "余额", "কত টাকা"]):
        return "balance"
    if any(p in text for p in ["report", "hisab", "হিসাব", "আজকের", "today", "খরচ"]):
        return "daily_report"
    if any(p in text for p in ["budget", "বাজেট", "预算"]):
        return "budget"
    if any(p in text for p in ["should i", "advice", "পরামর্শ", "建议", "কিনব", "invest"]):
        return "advice"
    if any(p in text for p in ["forecast", "predict", "পূর্বাভাস", "预测"]):
        return "forecast"
    if is_financial_topic(text):
        return "financial"
    return "non_financial"


def generate_response(text, lang="bn"):
    name = USER_PROFILE["name"]
    balance = USER_PROFILE["balance"]
    today_spent = USER_PROFILE["today_spent"]

    intent = detect_intent(text)

    if intent == "greeting":
        return {
            "bn": f"হ্যালো {name}! আপনার ব্যালেন্স {balance} ETH। কী করতে পারি আপনার জন্য?",
            "en": f"Hello {name}! Your balance is {balance} ETH. How can I help?",
            "zh": f"你好 {name}！您的余额为 {balance} ETH。有什么可以帮您？",
        }.get(lang, f"হ্যালো {name}!")

    if intent == "how_are_you":
        return {
            "bn": f"আমি ভালো আছি, ধন্যবাদ! আপনার ব্যালেন্স {balance} ETH। আজ {today_spent} ETH খরচ হয়েছে। কিছু দরকার?",
            "en": f"I'm great, thanks! Your balance is {balance} ETH. You spent {today_spent} ETH today.",
            "zh": f"我很好，谢谢！您的余额为 {balance} ETH。今天花费了 {today_spent} ETH。",
        }.get(lang, "আমি ভালো আছি!")

    if intent == "thanks":
        return {
            "bn": f"স্বাগতম, {name}!",
            "en": f"You're welcome, {name}!",
            "zh": f"不客气，{name}！",
        }.get(lang, "স্বাগতম!")

    if intent == "farewell":
        return {
            "bn": f"বিদায়, {name}! আবার কথা হবে।",
            "en": f"Goodbye, {name}! See you soon.",
            "zh": f"再见，{name}！",
        }.get(lang, "বিদায়!")

    if intent == "non_financial":
        return {
            "bn": "আমি একজন আর্থিক সহকারী। আমি টাকা, বিল, বাজেট, বিনিয়োগ, ক্রিপ্টো — এই বিষয়ে সাহায্য করতে পারি। আপনি কী করতে চান?",
            "en": "I'm a financial assistant. I can help with money, bills, budgets, investments, crypto. What would you like to do?",
            "zh": "我是财务助手。我可以帮助您处理金钱、账单、预算、投资、加密货币。",
        }.get(lang, "আমি আর্থিক সহকারী।")

    return None


def update_profile(name=None, balance=None, today_spent=None):
    if name:
        USER_PROFILE["name"] = name
    if balance is not None:
        USER_PROFILE["balance"] = balance
    if today_spent is not None:
        USER_PROFILE["today_spent"] = today_spent
