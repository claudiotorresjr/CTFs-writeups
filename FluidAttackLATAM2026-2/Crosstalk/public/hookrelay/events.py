"""Background event sources.

Two loops run in daemon threads:

* ``_user_event_loop`` synthesises mock ``user.*`` and ``webhook.*`` events
  every few seconds so a regular tenant's dashboards have something to
  display. These are dispatched via :func:`dispatch_event` so they go
  through the normal per-subscription filter.

* ``_heartbeat_loop`` emits a platform-health beacon every minute. Per
  the SLA contract these are routed through
  :func:`record_system_broadcast` so every tenant can audit them
  regardless of subscription filter.
"""

import secrets
import threading
import time

from hookrelay.audit import record_system_broadcast
from hookrelay.config import HEARTBEAT_TOKEN
from hookrelay.dispatch import dispatch_event


def _user_event_loop():
    counter = 0
    while True:
        counter += 1
        try:
            for event in _synthetic_user_events(counter):
                dispatch_event(event)
        except Exception:
            pass
        time.sleep(7)


def _synthetic_user_events(counter: int):
    yield {
        "id": secrets.token_hex(8),
        "type": "user.created",
        "actor": {"role": "platform", "tenant": "_synthetic"},
        "payload": {"user_id": f"usr_synth_{counter}"},
        "ts": int(time.time()),
    }
    yield {
        "id": secrets.token_hex(8),
        "type": "webhook.delivered",
        "actor": {"role": "platform"},
        "payload": {"endpoint": "https://example.com/synthetic", "latency_ms": 42},
        "ts": int(time.time()),
    }


def _heartbeat_loop():
    while True:
        try:
            event = {
                "id": secrets.token_hex(8),
                "type": "system.heartbeat",
                "actor": {
                    "role": "system",
                    "context": {
                        "continuation_id": HEARTBEAT_TOKEN,
                    },
                },
                "region": "us-east-1",
                "ts": int(time.time()),
            }
            record_system_broadcast(event)
        except Exception:
            pass
        time.sleep(60)


def start_background_loops() -> None:
    threading.Thread(target=_user_event_loop, daemon=True).start()
    threading.Thread(target=_heartbeat_loop, daemon=True).start()
