# automation/app/auth_server.py
from pathlib import Path
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
    우측 상단 'Search for local users' 입력창이 들어있는 정확한 root(page 또는 frame)를 찾아서 반환.
    FortiAuthenticator UI는 메인 콘텐츠가 iframe에 들어가는 경우가 많으므로 모든 frame을 순회한다.
    """
    candidates = [
        "input[placeholder='Search for local users']",
        "input[placeholder*='Search for local users']",
        "input[placeholder*='Search']",
        "input[type='search']",
    ]

    # 1) 메인 프레임 먼저 확인
    for sel in candidates:
        loc = page.locator(sel)
        if loc.count():
            try:
                loc.first.wait_for(state="visible", timeout=2500)
                return page
            except Exception:
                pass

    # 2) 모든 iframe에서 검색
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
    # 1) 로그인
    page.goto(AUTH_URL, wait_until="domcontentloaded")
    _first(page, S.LOGIN_USER).fill(AUTH_USER)
    _first(page, S.LOGIN_PASS).fill(AUTH_PASS)
    _first(page, S.LOGIN_SUBMIT).click()
    page.wait_for_load_state("networkidle")

    # 2) 좌측 메뉴로 Local Users 이동 (텍스트 매칭이 더 안정적)
    page.locator("a:has-text('Authentication')").first.click()
    page.locator("a:has-text('User Management')").first.click()
    page.locator("a:has-text('Local Users')").first.click()

    # 3) 본문 프레임(main_frame) 안에서 테이블 로드까지 대기
    fr = page.frame(name="main_frame")
    if not fr:
        raise RuntimeError("main_frame 프레임을 찾을 수 없습니다.")
    fr.locator("#result_list thead").wait_for(state="visible", timeout=15000)

    # 4) DataTables 검색창 찾기 (placeholder 여부와 무관하게)
    search = fr.locator(
        "div.dataTables_filter input, input[aria-controls], input[type='search']"
    ).first
    search.wait_for(state="visible", timeout=8000)

    # 5) 검색 수행 (DataTables는 타이핑만 해도 필터됨; Enter 불필요)
    search.click()
    search.press("Control+A")
    search.press("Delete")
    search.fill(app_id)
    page.wait_for_timeout(600)  # 필터 반영 대기

    # 6) User 컬럼이 '정확히' app_id인 행만 선택 (부분일치 방지)
    row = fr.locator(
        f"xpath=//table//tbody//tr[normalize-space(td[1])='{app_id}']"
    ).first
    row.wait_for(state="visible", timeout=10000)

    # 7) 'First Name' 컬럼 인덱스 동적 계산 후 값 추출
    headers = [h.strip() for h in fr.locator("xpath=//table//thead//th").all_inner_texts()]
    try:
        col_idx = headers.index("First Name") + 1  # nth-child는 1부터
    except ValueError:
        col_idx = 2  # 폴백: 스샷 기준 2번째 컬럼

    first_name = row.locator(f"xpath=td[{col_idx}]").inner_text().strip()
    return first_name


