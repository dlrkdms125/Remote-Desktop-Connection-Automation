from playwright.sync_api import sync_playwright

def launch(headless=True, channel="msedge", executable_path=None):
    pw = sync_playwright().start()
    if executable_path:
        browser = pw.chromium.launch(executable_path=executable_path, headless=headless)
    else:
        browser = pw.chromium.launch(channel=channel, headless=headless)
    ctx = browser.new_context(ignore_https_errors=True)
    page = ctx.new_page()
    return pw, browser, ctx, page

def close(pw, browser, ctx):
    try:
        ctx.close()
    finally:
        try:
            browser.close()
        finally:
            pw.stop()
