"""
Sentinel Wallet AI - Complete Agent with NLP, Voice, and Blockchain Features.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web3 import Web3
from dotenv import load_dotenv

# Features
from features.accounting import log_transaction, log_decision, daily_report
from features.self_correction import attempt_with_correction, set_last_rejection_reason
from features.verifier import verify_transaction
from features.simulation import simulate_transaction, print_simulation
from features.session_budget import (
    check_session_budget, record_session_spend,
    print_session_status
)
from features.budget import get_budget_status
from features.forecasting import forecast_monthly
from features.advice import advise_purchase
from features.bill_payment import get_scheduler
from features.audit_trail import add_audit_entry, verify_chain
from features.nlp_parser import (
    parse_command, register_contact, print_help, resolve_recipient
)
from features.portfolio import print_portfolio
from features.anomaly_detector import check_anomaly, record_transaction as record_anomaly
from features.prompt_injection_guard import scan_for_injection, sanitize_input
from features.proof_gated_signing import generate_proof, print_proof
from features.drain_taxonomy import check_drain_risk
from features.compliance import get_compliance, check_compliance
from features.storage import update_state, get_state_value
from features.swap import simulate_swap
from features.currency_converter import convert, print_conversion
from features.multilingual_response import generate_response_for_command
from features.multilingual_voice import detect_language

# Blockchain features
from features.wallet_manager import create_agent_wallet, load_wallet, print_wallet_info
from features.deposit import calculate_deposit, print_deposit_address
from features.withdraw import calculate_withdraw, withdraw_to_external
from features.qr_code import print_qr_ascii
from features.gas_estimator import estimate_gas
from features.multi_chain import list_chains

# Load .env
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# Config
GANACHE_URL = os.getenv("GANACHE_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
AGENT_ADDRESS = os.getenv("AGENT_ADDRESS")
AGENT_PRIVATE_KEY = os.getenv("AGENT_PRIVATE_KEY")
OWNER_ADDRESS = os.getenv("OWNER_ADDRESS")
OWNER_PRIVATE_KEY = os.getenv("OWNER_PRIVATE_KEY")
RECIPIENT_ADDRESS = os.getenv("RECIPIENT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
print(f"Connected: {w3.is_connected()}")

abi_path = os.path.join(os.path.dirname(__file__), "contract_abi.json")
with open(abi_path) as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

WHITELIST = [RECIPIENT_ADDRESS]

register_contact("rahim", RECIPIENT_ADDRESS)
register_contact("recipient", RECIPIENT_ADDRESS)

get_compliance().verify_kyc(RECIPIENT_ADDRESS)


def check_balance(address):
    return w3.from_wei(w3.eth.get_balance(address), "ether")


def fund_contract(amount_eth):
    amount_wei = w3.to_wei(amount_eth, "ether")
    nonce = w3.eth.get_transaction_count(OWNER_ADDRESS)
    txn = {
        "from": OWNER_ADDRESS, "to": CONTRACT_ADDRESS, "value": amount_wei,
        "nonce": nonce, "gas": 100000,
        "gasPrice": w3.to_wei("20", "gwei"), "chainId": 1337
    }
    signed = w3.eth.account.sign_transaction(txn, private_key=OWNER_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Funded: {amount_eth} ETH. TX: {receipt.transactionHash.hex()[:16]}...")


def pre_check(to, amount_eth):
    amount_wei = w3.to_wei(amount_eth, "ether")
    return contract.functions.preCheck(to, amount_wei).call()


def execute_transaction(to, amount_eth, user_input=""):
    amount_wei = w3.to_wei(amount_eth, "ether")
    
    # Prompt injection scan
    ok, msg = scan_for_injection(user_input)
    if not ok:
        print(f"REJECTED (Injection): {msg}")
        log_transaction("", to, amount_eth, "REJECTED", msg)
        return None
    
    # Verifier
    verified, verify_reason = verify_transaction(
        to, amount_eth, whitelist=WHITELIST, max_amount=0.01
    )
    if not verified:
        print(f"REJECTED (Verifier): {verify_reason}")
        set_last_rejection_reason(verify_reason)
        log_transaction("", to, amount_eth, "REJECTED", f"VERIFIER: {verify_reason}")
        add_audit_entry("REJECTED_VERIFIER", {"to": to, "amount": amount_eth, "reason": verify_reason})
        return None
    
    # Anomaly
    ok, msg = check_anomaly(amount_eth)
    if not ok:
        print(f"REJECTED (Anomaly): {msg}")
        set_last_rejection_reason(msg)
        log_transaction("", to, amount_eth, "REJECTED", msg)
        return None
    
    # Compliance
    compliant, checks = check_compliance(to, amount_eth)
    if not compliant:
        print(f"REJECTED (Compliance)")
        set_last_rejection_reason("COMPLIANCE_FAILED")
        log_transaction("", to, amount_eth, "REJECTED", "COMPLIANCE_FAILED")
        return None
    
    # Session budget
    session_ok, session_reason = check_session_budget(amount_eth, session_limit_eth=0.05)
    if not session_ok:
        print(f"REJECTED (Session): {session_reason}")
        set_last_rejection_reason(session_reason)
        log_transaction("", to, amount_eth, "REJECTED", session_reason)
        return None
    
    # Contract pre-check
    allowed, reason = pre_check(to, amount_eth)
    if not allowed:
        print(f"REJECTED (Contract): {reason}")
        set_last_rejection_reason(reason)
        log_transaction("", to, amount_eth, "REJECTED", reason)
        add_audit_entry("REJECTED_CONTRACT", {"to": to, "amount": amount_eth, "reason": reason})
        return None
    
    # Simulation
    sim = simulate_transaction(w3, contract, AGENT_ADDRESS, to, amount_eth)
    if not print_simulation(sim, to, amount_eth):
        set_last_rejection_reason(f"SIMULATION: {sim.reason}")
        log_transaction("", to, amount_eth, "REJECTED", f"SIMULATION: {sim.reason}")
        return None
    
    # Proof-gated
    proof_checks = [
        {"name": "VERIFIER", "passed": True, "details": "OK"},
        {"name": "COMPLIANCE", "passed": True, "details": "OK"},
        {"name": "SESSION_BUDGET", "passed": True, "details": "OK"},
        {"name": "CONTRACT_PRECHECK", "passed": True, "details": "OK"},
        {"name": "SIMULATION", "passed": True, "details": "OK"},
    ]
    proof = generate_proof(to, amount_eth, proof_checks)
    print_proof(proof)
    
    if not proof.is_valid():
        print("REJECTED: Proof invalid")
        return None
    
    # Execute
    nonce = w3.eth.get_transaction_count(AGENT_ADDRESS)
    txn = contract.functions.checkAndExecute(to, amount_wei).build_transaction({
        "from": AGENT_ADDRESS, "nonce": nonce, "gas": 200000,
        "gasPrice": w3.to_wei("20", "gwei"), "chainId": 1337
    })
    signed = w3.eth.account.sign_transaction(txn, private_key=AGENT_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    tx_hex = receipt.transactionHash.hex()
    print(f"SUCCESS! TX: {tx_hex[:16]}...")
    
    record_session_spend(amount_eth, tx_hex)
    record_anomaly(amount_eth)
    log_transaction(tx_hex, to, amount_eth, "SUCCESS")
    log_decision(user_input, {"to": to, "amount": amount_eth}, "OK", "EXECUTED")
    add_audit_entry("EXECUTED", {"to": to, "amount": amount_eth, "tx": tx_hex})
    
    return tx_hex


def handle_command(text):
    print(f"\n[NLP] User: {text}")
    text = sanitize_input(text)
    
    result = parse_command(text)
    action = result["action"]
    params = result.get("params", {})
    
    print(f"[NLP] Action: {action} | Params: {params}")
    
    if action == "transfer":
        if params.get("error"):
            print(f"ERROR: {params['error']}")
            return
        to = params.get("recipient_address")
        amount = params.get("amount")
        if not to or not amount:
            print("ERROR: Missing recipient or amount")
            return
        execute_transaction(to, amount, text)
    
    elif action == "check_balance":
        print(f"\nBalance: {check_balance(AGENT_ADDRESS)} ETH")
    
    elif action == "daily_report":
        daily_report()
    
    elif action == "budget_status":
        get_budget_status()
    
    elif action == "forecast":
        forecast_monthly()
    
    elif action == "advice":
        amount = params.get("amount", 0)
        advise_purchase(amount, 0.3, "purchase")
    
    elif action == "swap":
        simulate_swap(
            params.get("from_token", "ETH"),
            params.get("to_token", "USDC"),
            params.get("amount", 0)
        )
    
    elif action == "convert_currency":
        amount = params.get("amount", 0)
        from_c = params.get("from_currency", "USD")
        to_c = params.get("to_currency", "BDT")
        result = convert(amount, from_c, to_c)
        print_conversion(result)
    
    elif action == "pay_bill_converted":
        amount = params.get("amount", 0)
        currency = params.get("currency", "USD").upper()
        
        if currency != "ETH":
            conv = convert(amount, currency, "ETH")
            if conv["success"]:
                eth_amount = conv["converted"]
                print(f"\n[Bill] {amount} {currency} = {eth_amount:.8f} ETH")
                
                if currency == "USD":
                    bdt_conv = convert(amount, "USD", "BDT")
                    if bdt_conv["success"]:
                        print(f"[Bill] {amount} USD = {bdt_conv['converted']:.2f} BDT")
                
                if eth_amount <= 0.009:
                    print(f"[Bill] Paying {eth_amount:.8f} ETH...")
                    execute_transaction(RECIPIENT_ADDRESS, eth_amount, f"Pay {amount} {currency} bill")
                else:
                    print(f"[Bill] Amount exceeds per-tx limit (0.009 ETH)")
            else:
                print(f"[Bill] Conversion failed")
    
    elif action == "create_wallet":
        create_agent_wallet("agent")
        print_wallet_info(w3, "agent")
    
    elif action == "deposit":
        amount = params.get("amount", 0)
        currency = params.get("currency", "USD")
        calculate_deposit(amount, currency, "ETH")
        print_deposit_address("agent")
    
    elif action == "withdraw":
        amount = params.get("amount", 0)
        currency = params.get("currency", "ETH")
        if currency.upper() == "ETH":
            calculate_withdraw(amount, "USD")
        else:
            print("[Withdraw] Only ETH withdrawal supported in demo")
    
    elif action == "show_address":
        wallet = load_wallet("agent")
        if wallet:
            print(f"\n[Wallet Address]")
            print(f"  {wallet['address']}")
            print_qr_ascii(wallet["address"])
        else:
            print("[Wallet] No agent wallet found. Create one first.")
    
    elif action == "estimate_gas":
        estimate_gas(w3, contract, AGENT_ADDRESS, RECIPIENT_ADDRESS, 0.009)
    
    elif action == "list_chains":
        list_chains()
    
    elif action == "help":
        print_help()
    
    else:
        print(f"Unknown command: {text}")
        print_help()


if __name__ == "__main__":
    print(f"\n=== INITIAL BALANCES ===")
    print(f"  Owner: {check_balance(OWNER_ADDRESS)} ETH")
    print(f"  Agent: {check_balance(AGENT_ADDRESS)} ETH")
    print(f"  Contract: {check_balance(CONTRACT_ADDRESS)} ETH")
    print(f"  Recipient: {check_balance(RECIPIENT_ADDRESS)} ETH")
    
    if float(check_balance(CONTRACT_ADDRESS)) < 0.05:
        print("\n--- Funding contract ---")
        fund_contract(0.1)
    
    # Interactive Mode
    print("\n" + "=" * 50)
    print("INTERACTIVE MODE - Type commands or 'quit'")
    print("=" * 50)
    print_help()
    
    while True:
        try:
            user_input = input("\n> You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            handle_command(user_input)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")