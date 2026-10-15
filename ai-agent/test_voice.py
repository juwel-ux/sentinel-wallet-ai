"""
Test multilingual voice input/output.
Speak in Bengali, English, or Chinese.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from features.multilingual_voice import (
    listen_command,
    speak_response,
    detect_language,
    get_language_name,
)


def main():
    print("=" * 50)
    print("VOICE TEST - Bengali, English, Chinese")
    print("=" * 50)
    print()
    print("Select language:")
    print("  1. English")
    print("  2. বাংলা (Bengali)")
    print("  3. 中文 (Chinese)")
    print()

    choice = input("Enter choice (1/2/3): ").strip()

    lang_map = {"1": "en", "2": "bn", "3": "zh"}
    lang = lang_map.get(choice, "en")

    print(f"\n🎤 Language: {get_language_name(lang)}")
    print("Say something... (e.g., 'balance' or 'ব্যালেন্স কত')")
    print()

    # Listen
    text = listen_command(lang)

    if not text:
        print("❌ No voice detected. Try again.")
        return

    print(f"\n✅ You said: {text}")

    # Detect language from text
    detected = detect_language(text)
    print(f"📊 Detected language: {get_language_name(detected)}")

    # Generate response in same language
    responses = {
        "bn": "আপনার কমান্ড পাওয়া গেছে",
        "zh": "已收到您的命令",
        "en": "Your command has been received",
    }

    response = responses.get(detected, responses["en"])
    print(f"\n🤖 AI Response: {response}")

    # Speak the response
    print("\n🔊 Speaking response...")
    speak_response(response, detected)

    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()

