"""
FastAPI server - Exposes AI agent as REST API.
Docker-aware: reads GANACHE_URL and OLLAMA_URL from environment.
"""

import sys
import os

# Add ai-agent folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "ai-agent"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import features
from features.nlp_parser import parse_command, register_contact
from features.multilingual_response import generate_response_for_command
from features.multilingual_voice import detect_language
from features.accounting import get_today_transactions
from features.budget import load_budget
from features.conversation import generate_response, update_profile
from features.llm_agent import llm_chat, get_llm_agent


app = FastAPI(title="Sentinel Wallet AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Lazy Web3 init ───
_w3 = None
_contract = None
_agent_address = None
_recipient_address = None
_execute_transaction = None
_check_balance = None


def _lazy_init():
    global _w3, _contract, _agent_address, _recipient_address
    global _execute_transaction, _check_balance

    if _w3 is not None:
        return

    import json
    from web3 import Web3
    from dotenv import load_dotenv

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)

    # Docker-aware URLs
    ganache_url = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")
    contract_address = os.getenv("CONTRACT_ADDRESS")
    _agent_address = os.getenv("AGENT_ADDRESS")
    _recipient_address = os.getenv("RECIPIENT_ADDRESS")
    agent_pk = os.getenv("AGENT_PRIVATE_KEY")

    print(f"[API] Connecting to Ganache: {ganache_url}")

    _w3 = Web3(Web3.HTTPProvider(ganache_url))

    if not _w3.is_connected():
        print(f"[API] ERROR: Cannot connect to Ganache at {ganache_url}")

    abi_path = os.path.join(
        os.path.dirname(__file__), "ai-agent", "contract_abi.json"
    )
    with open(abi_path) as f:
        abi = json.load(f)

    _contract = _w3.eth.contract(
        address=_w3.to_checksum_address(contract_address),
        abi=abi,
    )

    def check_balance(addr):
        return _w3.from_wei(_w3.eth.get_balance(addr), "ether")

    def execute_transaction(to, amount_eth, user_input=""):
        amount_wei = _w3.to_wei(amount_eth, "ether")

        # Pre-check
        allowed, reason = _contract.functions.preCheck(to, amount_wei).call()
        if not allowed:
            return None

        # Execute
        nonce = _w3.eth.get_transaction_count(_agent_address)
        txn = _contract.functions.checkAndExecute(to, amount_wei).build_transaction({
            "from": _agent_address,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": _w3.to_wei("20", "gwei"),
            "chainId": 1337,
        })

        signed = _w3.eth.account.sign_transaction(txn, private_key=agent_pk)
        tx_hash = _w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = _w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()

    _check_balance = check_balance
    _execute_transaction = execute_transaction

    # Register default contact
    register_contact("rahim", _recipient_address)

    # Init LLM agent
    get_llm_agent()


# ─── Models ───
class CommandRequest(BaseModel):
    text: str
    language: str = "auto"


class CommandResponse(BaseModel):
    action: str
    response: str
    language: str
    success: bool
    tx_hash: str = ""
    details: dict = {}


# ─── Routes ───
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Sentinel Wallet AI",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    _lazy_init()
    return {
        "api": "ok",
        "ganache": _w3.is_connected() if _w3 else False,
        "agent": _agent_address,
    }


@app.get("/balance")
def get_balance():
    _lazy_init()
    return {
        "balance_eth": float(_check_balance(_agent_address)),
        "agent_address": _agent_address,
    }


@app.post("/command", response_model=CommandResponse)
def process_command(req: CommandRequest):
    _lazy_init()

    text = req.text.strip()
    lang = req.language

    if lang == "auto":
        lang = detect_language(text)

    # Update context
    balance = float(_check_balance(_agent_address))
    update_profile(balance=balance)

    context = {
        "name": "Emdad",
        "balance": balance,
        "today_spent": 0.018,
        "budget_used": 60,
    }

    # ─── Step 1: Try NLP command ───
    result = parse_command(text)
    action = result["action"]
    params = result.get("params", {})

    # Transfer
    if action == "transfer":
        if params.get("error"):
            return CommandResponse(
                action=action,
                response=generate_response_for_command(
                    "transfer", params, lang, success=False,
                    reason=params["error"],
                ),
                language=lang,
                success=False,
            )

        to = params.get("recipient_address")
        amount = params.get("amount")

        if not to or not amount:
            return CommandResponse(
                action=action,
                response=generate_response_for_command(
                    "transfer", params, lang, success=False,
                    reason="Missing data",
                ),
                language=lang,
                success=False,
            )

        tx = _execute_transaction(to, amount, text)

        if tx:
            return CommandResponse(
                action=action,
                response=generate_response_for_command(
                    "transfer", params, lang, success=True, tx=tx,
                ),
                language=lang,
                success=True,
                tx_hash=tx,
                details={"to": to, "amount": amount},
            )
        else:
            return CommandResponse(
                action=action,
                response=generate_response_for_command(
                    "transfer", params, lang, success=False,
                    reason="Rejected by constraints",
                ),
                language=lang,
                success=False,
            )

    # Balance
    if action == "check_balance":
        balance = float(_check_balance(_agent_address))
        return CommandResponse(
            action=action,
            response=generate_response_for_command(
                "check_balance", {}, lang, balance=balance,
            ),
            language=lang,
            success=True,
            details={"balance": balance},
        )

    # Daily report
    if action == "daily_report":
        txs = get_today_transactions()
        total = sum(t["amount_eth"] for t in txs)
        return CommandResponse(
            action=action,
            response=generate_response_for_command(
                "daily_report", {}, lang, count=len(txs), total=total,
            ),
            language=lang,
            success=True,
            details={"count": len(txs), "total": total},
        )

    # Budget
    if action == "budget_status":
        budget = load_budget()
        allocated = sum(budget["categories"].values())
        return CommandResponse(
            action=action,
            response=generate_response_for_command(
                "budget_status", {}, lang,
                income=budget["monthly_income_eth"],
                allocated=allocated,
            ),
            language=lang,
            success=True,
        )

    # ─── Step 2: LLM for conversational ───
    llm_response = llm_chat(text, context, lang)
    if llm_response:
        return CommandResponse(
            action="llm_conversation",
            response=llm_response,
            language=lang,
            success=True,
        )

    # ─── Step 3: Rule-based fallback ───
    conv_response = generate_response(text, lang)
    if conv_response:
        return CommandResponse(
            action="conversation",
            response=conv_response,
            language=lang,
            success=True,
        )

    # ─── Step 4: Unknown ───
    fallbacks = {
        "bn": "দুঃখিত, আমি বুঝতে পারিনি। আবার বলুন।",
        "en": "Sorry, I didn't understand. Please try again.",
        "zh": "抱歉，我不明白。请再试一次。",
    }
    return CommandResponse(
        action="unknown",
        response=fallbacks.get(lang, fallbacks["en"]),
        language=lang,
        success=False,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)