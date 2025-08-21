# automation/app/vpn_login.py
from playwright.sync_api import TimeoutError as PWTimeout
from . import selectors as S
from .config import VPN1_URL, VPN2_URL, VPN_USER, VPN_PASS

def _first(page, sels, timeout=4000):
    for s in sels:
        try:
            el = page.locator(s)
            el.wait_for(state="visible", timeout=timeout)
            return el
        except PWTimeout:
            pass
    raise RuntimeError(f"no visible element: {sels}")

def login_vpn(page, which: str):
    url = VPN1_URL if which.upper() == "VPN1" else VPN2_URL
    page.goto(url, wait_until="domcontentloaded")
    _first(page, S.VPN_LOGIN_USER).fill(VPN_USER)
    _first(page, S.VPN_LOGIN_PASS).fill(VPN_PASS)
    _first(page, S.VPN_LOGIN_SUBMIT).click()
    page.wait_for_load_state("networkidle")

    # FortiOS 팝업 처리 (OK 버튼)
    try:
        ok_btn = page.locator("button.ok-button.primary").first
        ok_btn.wait_for(state="visible", timeout=5000)
        ok_btn.click()

    except Exception:
        print("[INFO] FortiOS 팝업 없음")
