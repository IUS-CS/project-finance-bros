import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:8000/")
    page.get_by_role("button", name="Manual Transaction Entry").click()
    page.get_by_role("textbox", name="Vendor name:").click()
    page.get_by_role("textbox", name="Vendor name:").fill("Speedway")
    page.get_by_role("spinbutton", name="Amount:").click()
    page.get_by_role("spinbutton", name="Amount:").fill("79")
    page.get_by_role("button", name="Submit").click()
    page.get_by_role("link", name="Edit Item").click()
    page.get_by_role("spinbutton", name="Amount:").click()
    page.get_by_role("spinbutton", name="Amount:").fill("89")
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Speedway $89.00 ")).to_be_visible()
    page.get_by_role("link", name="Delete Item").click()


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
