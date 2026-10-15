"""
Multilingual Voice module - Listen and respond in Bengali, English, Chinese.
"""


LANGUAGES = {
    "en": {"speech": "en-US", "tts": "en", "name": "English"},
    "bn": {"speech": "bn-BD", "tts": "bn", "name": "বাংলা"},
    "zh": {"speech": "zh-CN", "tts": "zh-CN", "name": "中文"},
}


def detect_language(text):
    """Simple language detection based on character sets."""
    bengali_chars = sum(1 for c in text if '\u0980' <= c <= '\u09FF')
    chinese_chars = sum(1 for c in text if '\u4E00' <= c <= '\u9FFF')
    
    if bengali_chars > 0:
        return "bn"
    if chinese_chars > 0:
        return "zh"
    return "en"


def get_language_name(lang_code):
    return LANGUAGES.get(lang_code, {}).get("name", "Unknown")


def get_tts_code(lang_code):
    return LANGUAGES.get(lang_code, {}).get("tts", "en")


def get_speech_code(lang_code):
    return LANGUAGES.get(lang_code, {}).get("speech", "en-US")


# Optional: Voice input/output (only if libraries installed)
def listen_command(lang="en"):
    """Listen for voice command. Requires SpeechRecognition + pyaudio."""
    try:
        import speech_recognition as sr
    except ImportError:
        print("[Voice] SpeechRecognition not installed. Run: pip install SpeechRecognition pyaudio")
        return None
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    speech_code = get_speech_code(lang)
    
    try:
        with microphone as source:
            print(f"[Voice] Listening in {get_language_name(lang)}...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        text = recognizer.recognize_google(audio, language=speech_code)
        print(f"[Voice] Heard: {text}")
        return text
    except Exception as e:
        print(f"[Voice] Error: {e}")
        return None


def speak_response(text, lang="en"):
    """Speak a response. Requires gTTS + mpg123."""
    try:
        from gtts import gTTS
    except ImportError:
        print("[Voice] gTTS not installed. Run: pip install gTTS")
        return False
    
    import os
    import tempfile
    
    tts_code = get_tts_code(lang)
    
    try:
        tts = gTTS(text=text, lang=tts_code, slow=False)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        os.system(f"mpg123 {temp_file.name} 2>/dev/null || ffplay -nodisp -autoexit {temp_file.name} 2>/dev/null")
        os.unlink(temp_file.name)
        return True
    except Exception as e:
        print(f"[Voice] TTS error: {e}")
        return False
