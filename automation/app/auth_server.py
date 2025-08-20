from playwright.sync_api import TimeoutError as PWTimeout
from . import selectors as S
from .config import AUTH_URL, AUTH_USER, AUTH_PASS


def _first(root, sels, timeout=8000):
    """
    sels: selector 문자열 목록 또는 locator-like 객체 목록
    root.locator(sel).first 가 보일 때까지 기다렸다가 반환
    """
    for s in sels:
        try:
            loc = root.locator(s).first if isinstance(s, str) else s.first
            loc.wait_for(state="visible", timeout=timeout)
            return loc
        except PWTimeout:
            pass
    raise RuntimeError(f"no visible element: {sels}")


def _find_search_root(page):
    """
    'Search for local users' 입력창이 들어있는 정확한 root(page 또는 frame)를 반환.
    """
    candidates = [
        "input[placeholder='Search for local users']",
        "input[placeholder*='Search']",
        "input[type='search']",
    ]

    # 메인 프레임
    for sel in candidates:
        loc = page.locator(sel)
        if loc.count():
            try:
                loc.first.wait_for(state="visible", timeout=2500)
                return page
            except Exception:
                pass

    # iframe 순회
    for fr in page.frames:
        for sel in candidates:
            loc = fr.locator(sel)
            if loc.count():
                try:
                    loc.first.wait_for(state="visible", timeout=2500)
                    return fr
                except Exception:
                    pass

    return None


def login_and_get_firstname(page, app_id: str) -> str:
    # 1) 인증 서버 로그인
    page.goto(AUTH_URL, wait_until="domcontentloaded")
    _first(page, S.AUTH_LOGIN_USER).fill(AUTH_USER)
    _first(page, S.AUTH_LOGIN_PASS).fill(AUTH_PASS)
    _first(page, S.AUTH_LOGIN_SUBMIT).click()
    page.wait_for_load_state("networkidle")

    # 2) 좌측 메뉴 → Local Users 이동
    page.locator("a:has-text('Authentication')").first.click()
    page.locator("a:has-text('User Management')").first.click()
    page.locator("a:has-text('Local Users')").first.click()

    # 3) 검색창이 있는 frame 찾기
    fr = page.frame(name="main_frame")
    if not fr:
        raise RuntimeError("main_frame 프레임을 찾을 수 없습니다.")
    fr.locator("#result_list thead").wait_for(state="visible", timeout=15000)

    # 4) 검색창 찾기
    search = _first(fr, S.LOCAL_USERS_SEARCH, timeout=15000)

    # 5) 검색 수행
    search.click()
    search.press("Control+A")
    search.press("Delete")
    search.fill(app_id)
    search.press("Enter")
    page.wait_for_timeout(1000)

    # 6) User 컬럼이 정확히 app_id인 행 선택
    row = fr.locator(
        f"xpath=//table[@id='result_list']//tbody//tr[td[2]/a[normalize-space(text())='{app_id}']]"
    ).first
    row.wait_for(state="visible", timeout=10000)

    # 7) 'First name' 값 추출
    first_name = row.locator("xpath=td[3]").inner_text().strip()
    return first_name
