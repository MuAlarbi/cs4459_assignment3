"""
CS 4459: Assignment 3 — Worker Service
Distributed Order Processing with Ticket-Based Coordination

Each worker is a FastAPI microservice that coordinates with peers
to ensure mutual exclusion when accessing the inventory service.
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
# Use state_lock to protect reads/writes to choosing and ticket.
# GET /state runs in a different thread than POST /start.
state_lock = threading.Lock()
choosing = False
ticket = 0


# ============================================================
#  TODO: Implement the coordination protocol and endpoints
# ============================================================

# --- Coordination Functions ---

def select_ticket():
    """
    Rule 1: Select a ticket number.
    """
    # TODO
    pass


def wait_for_turn():
    """
    Rule 2: Wait until it's safe to enter the critical section.
    """
    # TODO
    pass


def acquire():
    """
    Acquire access to the critical section.
    """
    # TODO
    pass


def release():
    """
    Rule 4: Release access to the critical section.
    """
    # TODO
    pass


# --- Endpoints ---

# TODO: Implement GET /state
# Must return: {"worker_id": ..., "choosing": ..., "ticket": ...}


# TODO: Implement POST /start
# Must: loop NUM_ORDERS times, acquire, get available item,
#        call POST /process-order with idempotency_key, release.
#        Stop early if no items available.
# Must return: {"status": "completed", "worker_id": ..., "orders_processed": ...}


# TODO: Implement GET /peers
# Must return: {"worker_id": ..., "peers": [...]}