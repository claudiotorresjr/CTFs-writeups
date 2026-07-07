from playwright.sync_api import sync_playwright
from threading import Semaphore

from utils import admin_session_id

semaphore = Semaphore(3)


def visit(url: str):
    semaphore.acquire()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        try:
            print("[bot] browser initialized")

            ctx = browser.new_context()
            ctx.add_cookies(
                [
                    {
                        "url": "http://127.0.0.1:5000/",
                        "name": "token",
                        "value": admin_session_id,
                    }
                ]
            )

            page = ctx.new_page()
            print(f"[*] visiting {url}")
            page.goto(url)

            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(10_000)

            browser.close()
            print(f"[+] visited {url}")
            return {"success": f"visited: {url}"}
        finally:
            semaphore.release()
