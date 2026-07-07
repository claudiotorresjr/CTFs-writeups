"""Audit log of webhook dispatches.

The log is per-tenant. Two write paths exist:

* ``record_dispatch`` is the regular-flow recorder used by ``dispatch_event``
  in :mod:`hookrelay.dispatch`. It writes one entry for each subscription
  whose filter matched the event being dispatched.

* ``record_system_broadcast`` is used for SLA-regulated platform health
  events that every tenant must be able to audit regardless of whether
  the event matched any subscription's filter. The contractual audit
  surface includes the URL each subscription *would* have been called on,
  so the rendered template is recorded alongside the system event.
"""

import threading
import time

from flask import Blueprint, jsonify

from hookrelay.auth import require_user_jwt
from hookrelay.subscriptions import iter_subscriptions
from hookrelay.templating import render

bp = Blueprint("audit", __name__)

_lock = threading.Lock()
_LOG: list[dict] = []
_MAX = 200


def _append(entry: dict) -> None:
    with _lock:
        _LOG.append(entry)
        if len(_LOG) > _MAX:
            del _LOG[: len(_LOG) - _MAX]


def record_dispatch(sub: dict, event: dict, rendered_url: str, status: str) -> None:
    _append({
        "timestamp": time.time(),
        "owner": sub["owner"],
        "subscription_id": sub["id"],
        "subscription_name": sub["name"],
        "event_type": event["type"],
        "rendered_url": rendered_url,
        "status": status,
    })


def record_system_broadcast(event: dict) -> None:
    """Append one audit row per active subscription for a system event.

    This is required by the SLA contract: tenants must be able to audit
    platform health beacons in their own audit feed. The rendered URL
    captures what the callback would have looked like for that
    subscription, so the auditor can verify the platform's intent.
    """
    for sub in iter_subscriptions():
        rendered = render(sub["url_template"], event)
        _append({
            "timestamp": time.time(),
            "owner": sub["owner"],
            "subscription_id": sub["id"],
            "subscription_name": sub["name"],
            "event_type": event["type"],
            "rendered_url": rendered,
            "status": "system_broadcast",
        })


@bp.route("/api/v2/audit/dispatches", methods=["GET"])
def list_dispatches():
    payload, err = require_user_jwt()
    if err:
        return err
    with _lock:
        owned = [e for e in _LOG if e["owner"] == payload["sub"]]
    return jsonify(owned[-50:])
