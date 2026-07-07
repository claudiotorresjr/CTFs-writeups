#!/usr/bin/env python3
"""
WhisperChat Desktop Client v1.4.2
Companion client for the WhisperChat messaging platform.

Usage:
    python whisper_client.py [--server URL]

The client connects to the WhisperChat API and allows you to
browse and send messages from the command line.
"""
import argparse
import json
import sys

import requests

API_BASE = "https://api.whisperchat.internal"
API_KEY = "fluidctf-api-2026-whispers"
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "WhisperChat/1.4.2 (Android 14; SDK 34)",
}


def fetch_messages(base_url):
    """Retrieve all messages from the server."""
    url = f"{base_url}/api/messages"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("messages", [])


def send_message(base_url, sender, recipient, body):
    """Send a new message."""
    url = f"{base_url}/api/messages"
    payload = {
        "sender": sender,
        "recipient": recipient,
        "body": body,
    }
    resp = requests.post(
        url, headers=HEADERS, json=payload, timeout=10
    )
    resp.raise_for_status()
    return resp.json()


def display_messages(messages):
    """Pretty-print messages to the console."""
    if not messages:
        print("  No messages found.")
        return
    for msg in messages:
        ts = msg.get("timestamp", "unknown")
        sender = msg.get("sender", "?")
        recipient = msg.get("recipient", "?")
        body = msg.get("body", "")
        print(f"  [{ts}] {sender} -> {recipient}: {body}")


def interactive_loop(base_url):
    """Main interactive menu."""
    print("=" * 50)
    print("  WhisperChat Desktop Client v1.4.2")
    print("=" * 50)
    print(f"  Server: {base_url}")
    print()

    while True:
        print("  1) View messages")
        print("  2) Send a message")
        print("  3) Quit")
        choice = input("\n  > ").strip()

        if choice == "1":
            print()
            try:
                messages = fetch_messages(base_url)
                display_messages(messages)
            except requests.RequestException as e:
                print(f"  Error: {e}")
            print()

        elif choice == "2":
            print()
            sender = input("  Your name: ").strip()
            recipient = input("  Recipient: ").strip()
            body = input("  Message: ").strip()
            if sender and recipient and body:
                try:
                    result = send_message(
                        base_url, sender, recipient, body
                    )
                    print("  Message sent.")
                except requests.RequestException as e:
                    print(f"  Error: {e}")
            else:
                print("  All fields are required.")
            print()

        elif choice == "3":
            print("  Goodbye.")
            break
        else:
            print("  Invalid option.\n")


def main():
    parser = argparse.ArgumentParser(
        description="WhisperChat Desktop Client"
    )
    parser.add_argument(
        "--server",
        default=API_BASE,
        help="API server URL (default: %(default)s)",
    )
    args = parser.parse_args()
    interactive_loop(args.server)


if __name__ == "__main__":
    main()
