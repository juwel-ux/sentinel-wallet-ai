"""
LLM-powered conversational agent using Ollama (local, free).
"""

import os

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


SYSTEM_PROMPT = """You are Sentinel Wallet AI, a friendly financial assistant for Emdad.

Your job:
- Help with money, crypto, bills, budgets, transactions
- Respond in the SAME language the user uses (Bengali, English, Chinese)
- Be casual, warm, and helpful
- Keep responses 1-3 sentences

Strict rules:
- ONLY help with financial topics
- If asked about weather, sports, relationships, or other non-financial topics,
  politely say: "I'm a financial assistant. I can help with money, bills, budgets, crypto."
- Never invent financial data
- Always be honest

Available actions you can suggest:
- Send ETH to contact
- Check balance
- Pay bills
- Show daily report
- Create budget
- Provide financial advice
- Swap tokens
- Convert currencies
- Show wallet address
- Estimate gas fee
"""


class OllamaAgent:
    def __init__(self, model="llama3.2:3b", base_url=None):
        self.model = model
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.available = OPENAI_AVAILABLE

        if self.available:
            try:
                self.client = OpenAI(
                    base_url=f"{self.base_url}/v1",
                    api_key="ollama",
                    timeout=60.0,
                )
                # Test connection
                self.client.models.list()
                print(f"[Ollama] Connected - Model: {model}")
            except Exception as e:
                print(f"[Ollama] Not running: {e}")
                self.available = False

    def chat(self, user_message, context=None, language="bn"):
        """Chat with the local LLM."""
        if not self.available:
            return None

        context = context or {}

        context_str = f"""
User: {context.get('name', 'Emdad')}
Balance: {context.get('balance', 0)} ETH
Today spent: {context.get('today_spent', 0)} ETH
Budget used: {context.get('budget_used', 0)}%
Language: {language}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "system", "content": context_str},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                max_tokens=150,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"[Ollama] Error: {e}")
            return None

    def is_financial(self, text):
        """Check if message is financial using LLM."""
        if not self.available:
            return True

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Reply only 'yes' or 'no'. Is this about finance, money, crypto, bills, budgets, or wallet?",
                    },
                    {"role": "user", "content": text},
                ],
                temperature=0,
                max_tokens=5,
            )
            answer = response.choices[0].message.content.strip().lower()
            return "yes" in answer

        except Exception:
            return True


_agent = None


def get_llm_agent(model="llama3.2:3b"):
    global _agent
    if _agent is None:
        _agent = OllamaAgent(model=model)
    return _agent


def llm_chat(user_message, context=None, language="bn"):
    """Chat with LLM, fallback to rule-based if unavailable."""
    agent = get_llm_agent()

    response = agent.chat(user_message, context, language)

    if response:
        return response

    # Fallback to rule-based conversation
    try:
        from features.conversation import generate_response
        fallback = generate_response(user_message, language)
        if fallback:
            return fallback
    except Exception:
        pass

    # Final fallback
    fallbacks = {
        "bn": "দুঃখিত, আমি বুঝতে পারিনি। আবার বলুন।",
        "en": "Sorry, I didn't understand. Please try again.",
        "zh": "抱歉，我不明白。请再试一次。",
    }
    return fallbacks.get(language, fallbacks["en"])


def is_financial_llm(text):
    agent = get_llm_agent()
    return agent.is_financial(text)
