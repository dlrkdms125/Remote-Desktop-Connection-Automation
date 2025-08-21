# automation/app/policy.py
from . import selectors as S

def search_policy(page, app_id: str):
    # 1. Policy & Objects → Firewall Policy로 이동
    page.locator("//span[contains(normalize-space(), 'Policy')]/ancestor::a").click()
    page.locator("a:has-text('Firewall Policy')").click()
    page.wait_for_load_state("networkidle")

    # 2. 검색창 찾기
    search = page.locator("input.search-input[placeholder='Search']").first
    search.wait_for(state="visible", timeout=10000)

    # 3. 검색 실행
    search.click()
    search.fill(app_id)
    search.press("Enter")
    page.wait_for_timeout(1000)

    # 4. 결과 행 반환
    row = page.locator(
        f"xpath=//table//tr[td[contains(normalize-space(), '{app_id}')]]"
    ).first
    row.wait_for(state="visible", timeout=10000)
    return row


def open_edit(page, row):
    row.click(button="right")
    page.get_by_role("menuitem", name="Edit", exact=False).click()
    page.wait_for_load_state("networkidle")

def set_source_dest(page, app_id: str, office_ip: str):
    src = page.locator(S.FIELD_SOURCE_INPUT).first
    src.fill(app_id); src.press("Enter")
    src.fill("EXT-User_Radius_GRP"); src.press("Enter")

    dst = page.locator(S.FIELD_DEST_INPUT).first
    dst.fill(office_ip); dst.press("Enter")

def create_onetime_schedule(page, name: str, s_date: str, s_time: str, e_date: str, e_time: str):
    page.locator(S.SCHEDULE_DROPDOWN).first.click()
    page.locator(S.BTN_CREATE).first.click()
    page.locator(S.BTN_ONE_TIME).first.click()

    page.locator(S.DIALOG_NAME).fill(name)
    page.locator(S.DIALOG_START_DATE).fill(s_date)
    page.locator(S.DIALOG_START_TIME).fill(s_time)
    page.locator(S.DIALOG_END_DATE).fill(e_date)
    page.locator(S.DIALOG_END_TIME).fill(e_time)
    page.locator(S.DIALOG_OK).click()

def enable_and_save(page):
    if page.locator(S.POLICY_ENABLE).count():
        page.locator(S.POLICY_ENABLE).first.click()
    page.locator(S.POLICY_OK).first.click()
    page.wait_for_load_state("networkidle")
