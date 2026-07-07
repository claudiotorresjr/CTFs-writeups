#!/usr/bin/env python3
"""Small local smoke test for the /report bot.

This is not the exploit. It only checks that the local bot accepts a URL and
returns the expected "visited" status before running solve_sheets.py.
"""

import argparse
from urllib.parse import quote

import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test for the Sheets report bot")
    parser.add_argument("--target", default="http://127.0.0.1:5000", help="local challenge URL")
    args = parser.parse_args()

    payload = "data:text/html," + quote("<h1>bot smoke</h1>")
    response = requests.get(
        f"{args.target.rstrip('/')}/report",
        params={"url": payload},
        timeout=25,
    )

    print(response.status_code)
    print(response.text[:200])


if __name__ == "__main__":
    main()
