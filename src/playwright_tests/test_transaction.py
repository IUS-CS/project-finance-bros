import re
import os
from playwright.sync_api import Playwright, sync_playwright, expect


def test_transaction_create(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless = False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:8000/")
    page.get_by_role("button", name = "Manual Transaction Entry").click()
    page.get_by_role("textbox", name = "Vendor name:").click()
    page.get_by_role("textbox", name = "Vendor name:").fill("Speedway")
    page.get_by_role("spinbutton", name = "Amount:").click()
    page.get_by_role("spinbutton", name = "Amount:").fill("80")
    page.get_by_role("button", name = "Submit").click()
    expect(page.get_by_text("Speedway $80.00 ")).to_be_visible()

      # ---------------------
    context.close()
    browser.close()

def test_transaction_delete(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:8000/")
    page.get_by_role("button", name="Saved Transactions").click()

    page.locator("li").filter(has_text="Speedway $80.00").first.get_by_role("link", name="Delete Item").click()

    page.wait_for_load_state("networkidle")
    expect(page.get_by_text("Speedway $80.00 ")).not_to_be_visible()

    # ---------------------
    context.close()
    browser.close()

def test_transaction_edit(playwright: Playwright) -> None:
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
    page.locator("li").filter(has_text="Speedway $79.00").first.get_by_role("link", name="Edit Item").click()
    page.get_by_role("spinbutton", name="Amount:").click()
    page.get_by_role("spinbutton", name="Amount:").fill("89")
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Speedway $89.00 ")).to_be_visible()
    page.locator("li").filter(has_text="Speedway $89.00").first.get_by_role("link", name="Delete Item").click()

def test_pdf_upload(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_media/March 19.pdf"))
    page.goto("http://127.0.0.1:8000/")
    page.get_by_role("button", name="Statement Reader").click()
    page.locator('input[name="file"]').set_input_files(file_path)
    page.get_by_role("button", name="Submit statement PDF").click()
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("SPEEDWAY 44109 MIDDLETOWN KY $10.68 ")).to_be_visible()
    page.locator("li").filter(has_text="SPEEDWAY 44109 MIDDLETOWN KY $10.68 ").first.get_by_role("link", name="Delete Item").click()



    # ---------------------
    context.close()
    browser.close()
