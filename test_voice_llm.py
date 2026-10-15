"""
Voice + LLM test - Speak and get AI response in your language.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "ai-agent"))

from features.multilingual_voice import (
    listen_command,
    speak_response,
    detect_language,
    get_language_name,
)
from features.llm_agent import llm_chat


def main():
    print("=" * 50)
    print("VOICE + LLM TEST")
    print("=" * 50)
    print()
    print("Select language:")
    print("  1. English")
    print("  2. বাংলা (Bengali)")
    print("  3. 中文 (Chinese)")
    print()

    choice = input("Enter choice (1/2/3): ").strip()
    lang_map = {"1": "en", "2": "bn", "3": "zh"}
    lang = lang_map.get(choice, "bn")

    print(f"\n🎤 Language: {get_language_name(lang)}")
    print("Type 'quit' to exit.\n")

    context = {
        "name": "Emdad",
        "balance": 99.97,
        "today_spent": 0.018,
        "budget_used": 60,
    }

    while True:
        input("Press ENTER to speak...")

        # Listen
        text = listen_command(lang)

        if not text:
            print("❌ No voice detected. Try again.")
            continue

        print(f"\n✅ You said: {text}")

        if text.lower().strip() in ["quit", "exit", "বিদায়", "再见"]:
            print("Goodbye!")
            break

        # Detect language
        detected = detect_language(text)
        print(f"📊 Language: {get_language_name(detected)}")

        # Get LLM response
        print("🤖 Thinking...")
        response = llm_chat(text, context, detected)

        if not response:
            response = "দুঃখিত, আমি বুঝতে পারিনি।"

        print(f"\n🤖 AI: {response}\n")

        # Speak response
        print("🔊 Speaking...")
        speak_response(response, detected)


if __name__ == "__main__":
    main()
