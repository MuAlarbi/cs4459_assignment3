"""
CS 4459: Assignment 3 — Worker Service
Distributed Order Processing with Message-Based Coordination

Each worker is a FastAPI microservice that coordinates with peers
using REQUEST/REPLY messages and Lamport logical clocks to ensure
mutual exclusion when accessing the inventory service.
"""

from fastapi import FastAPI
import os
import requests
import time
import threading

app = FastAPI()

# --- Environment Variables (set by Docker Compose — DO NOT MODIFY) ---
WORKER_ID = int(os.environ["WORKER_ID"])
NUM_WORKERS = int(os.environ["NUM_WORKERS"])
NUM_ORDERS = int(os.environ.get("NUM_ORDERS", "50"))
INVENTORY_URL = os.environ.get("INVENTORY_URL", "http://inventory-service:8000")


def get_peer_url(worker_id: int) -> str:
    """Returns the base URL for a peer worker."""
    return f"http://worker-{worker_id}:{5000 + worker_id}"


# --- Coordination State ---
# Use state_lock to protect all coordination state.
# Multiple threads access this state: the /start processing loop,
# the /request handler, and the /reply handler.

state_lock = threading.Lock()
clock = 0
state = "RELEASED"          # "RELEASED", "WANTED", or "HELD"
request_timestamp = None    # Clock value when we requested access
replies_received = 0        # Count of REPLY messages for current request
deferred_queue = []         # Worker IDs whose REPLY we deferred

# Event to signal when all replies have been received.
# acquire() waits on this; the /reply handler sets it.
all_replies = threading.Event()


# ============================================================
#  TODO: Implement the coordination protocol and endpoints
# ============================================================

# --- Coordination Functions ---

def acquire():
    """
    Rule 1: Request access to the critical section.
    Sets state to WANTED, increments clock, records timestamp,
    sends REQUEST to all peers, waits for N-1 REPLYs.
    """
    # TODO
    pass


def release():
    """
    Rule 4: Release access to the critical section.
    Sets state to RELEASED, sends REPLY to all deferred peers.
    """
    # TODO
    pass


# --- Message Handlers ---

# TODO: Implement POST /request
# Receives: {"timestamp": int, "sender_id": int}
# Rule 2: Decide whether to reply immediately or defer.


# TODO: Implement POST /reply
# Receives: {"timestamp": int, "sender_id": int}
# Rule 3: Update clock, increment replies_received.
# If replies_received == NUM_WORKERS - 1, signal all_replies.


# --- Other Endpoints ---

# TODO: Implement GET /state
# Must return: {"worker_id": ..., "clock": ..., "state": ...,
#               "request_timestamp": ..., "replies_received": ...,
#               "deferred_count": ...}


# TODO: Implement POST /start
# Must: loop NUM_ORDERS times, acquire, get available item,
#        call POST /process-order with idempotency_key, release.
#        Stop early if no items available.
# Must return: {"status": "completed", "worker_id": ..., "orders_processed": ...}


# TODO: Implement GET /peers
# Must return: {"worker_id": ..., "peers": [...]}