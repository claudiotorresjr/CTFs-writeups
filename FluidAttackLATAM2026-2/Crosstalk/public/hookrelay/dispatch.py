"""Webhook event dispatcher.

Per-subscription delivery filtered by event type. For each subscription
whose filter matches the event, the URL template is rendered against the
event payload and recorded in the audit log. (Outbound HTTP delivery is
disabled in the CTFae sandbox; the audit row is the canonical record of
the dispatch.)
"""

from hookrelay.audit import record_dispatch
from hookrelay.subscriptions import iter_subscriptions
from hookrelay.templating import render


def _filter_matches(pattern: str, event_type: str) -> bool:
    if pattern.endswith(".*"):
        return event_type.startswith(pattern[:-1])
    return pattern == event_type


def dispatch_event(event: dict) -> None:
    """Notify every subscription whose filter matches `event`."""
    for sub in iter_subscriptions():
        if not _filter_matches(sub["filter"], event["type"]):
            continue
        try:
            rendered = render(sub["url_template"], event)
        except Exception:
            continue
        record_dispatch(sub, event, rendered, "delivered")
