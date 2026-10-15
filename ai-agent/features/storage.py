"""
Persistent Storage module - Save and load agent state.
"""

import json
import os
from datetime import datetime


STORAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(STORAGE_DIR, exist_ok=True)

STATE_FILE = os.path.join(STORAGE_DIR, "agent_state.json")


def save_state(state):
    """Save agent state to file."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)
    print(f"[Storage] State saved: {STATE_FILE}")


def load_state():
    """Load agent state from file."""
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE) as f:
        return json.load(f)


def update_state(key, value):
    """Update a single key in state."""
    state = load_state()
    state[key] = value
    save_state(state)


def get_state_value(key, default=None):
    state = load_state()
    return state.get(key, default)


def save_snapshot(name, data):
    """Save a named snapshot."""
    filepath = os.path.join(STORAGE_DIR, f"{name}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"[Storage] Snapshot saved: {filepath}")


def load_snapshot(name):
    """Load a named snapshot."""
    filepath = os.path.join(STORAGE_DIR, f"{name}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath) as f:
        return json.load(f)


def list_snapshots():
    """List all snapshots."""
    if not os.path.exists(STORAGE_DIR):
        return []
    return [f[:-5] for f in os.listdir(STORAGE_DIR) if f.endswith(".json")]
