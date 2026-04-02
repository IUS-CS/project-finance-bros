import re
from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    current_date_str = datetime.now().strftime("%B %-d, %Y")
    page.goto("http://127.0.0.1:8000/")
    page.get_by_role("button", name="Saved Transactions").click()
    page.get_by_role("link", name="Delete Item").click()
    expect(page.get_by_text("Speedway $80.00 " + current_date_str)).not_to_be_visible()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
  run(playwright)
