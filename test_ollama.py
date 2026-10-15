import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "ai-agent"))

from features.llm_agent import llm_chat

context = {
    "name": "Emdad",
    "balance": 99.97,
    "today_spent": 0.018,
    "budget_used": 60,
}

tests = [
    "Hello",
    "কেমন আছো?",
    "আজ আমার মন ভালো নেই",
    "আমার বন্ধুকে ৫ ডলার পাঠাতে হবে",
    "আজ আবহাওয়া কেমন?",
    "আমি কি ০.১ ETH দিয়ে NFT কিনব?",
    "তোমার নাম কি?",
    "ধন্যবাদ",
]

for text in tests:
    print(f"\nUser: {text}")
    response = llm_chat(text, context, "bn")
    if response:
        print(f"AI: {response}")
    else:
        print("AI: (Ollama not running)")
    print("-" * 50)
