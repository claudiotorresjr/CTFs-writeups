"""URL template rendering for webhook subscription callbacks.

Templates use the form ``{{path.to.field}}`` and resolve against an event
context dict. Missing paths render as the empty string.
"""

import re

_TOKEN = re.compile(r"\{\{\s*([A-Za-z0-9_.]+)\s*\}\}")


def _resolve(path: str, ctx) -> str:
    cur = ctx
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return ""
        if cur is None:
            return ""
    if isinstance(cur, (dict, list)):
        return ""
    return str(cur)


def render(template: str, ctx) -> str:
    return _TOKEN.sub(lambda m: _resolve(m.group(1), ctx), template)
