import argparse
from automation.app.browser import launch, close
from automation.app.auth_server import login_and_get_firstname
from automation.app.vpn_login import login_vpn
from automation.app.policy import (
    goto_firewall_policy, search_policy, open_edit,
    set_source_dest, create_onetime_schedule, enable_and_save
)
from automation.app.config import build_schedule_name, split_date_time

def prompt_if_missing(args):
    if not args.app_id:
        args.app_id = input("신청ID: ").strip()
    if not args.start:
        args.start = input('시작일시(예: 20250701 07): ').strip()
    if not args.end:
        args.end = input('종료일시(예: 20250701 22): ').strip()
    if not args.office_ip:
        args.office_ip = input('사무실 PC IP: ').strip()
    return args

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app-id")
    ap.add_argument("--start", help="YYYYMMDD HH")
    ap.add_argument("--end", help="YYYYMMDD HH")
    ap.add_argument("--office-ip")
    ap.add_argument("--headful", action="store_true")
    args = ap.parse_args()

    # 인자 없으면 터미널에서 입력
    args = prompt_if_missing(args)

    pw, browser, ctx, page = launch(headless=not args.headful)
    try:
        print("[1] 인증서버 로그인 & First Name 확인")
        first_name = login_and_get_firstname(page, args.app_id)
        print("   First Name =", first_name)

        if first_name.upper() in ("VPN1", "VPN2"):
            print(f"[2] {first_name} 로그인")
            login_vpn(page, first_name)
        else:
            print("[WARN] VPN1/VPN2 아님. 계속 진행할지 확인 필요")

        print("[3] Policy & Objects → Firewall Policy 이동, 검색/편집")
        goto_firewall_policy(page)
        row = search_policy(page, args.app_id)
        open_edit(page, row)

        print("[4] Source/Destination 설정")
        set_source_dest(page, args.app_id, args.office_ip)

        print("[5] One-Time Schedule 생성")
        name = build_schedule_name(args.start, args.end)
        s_date, s_time = split_date_time(args.start)
        e_date, e_time = split_date_time(args.end)
        create_onetime_schedule(page, name, s_date, s_time, e_date, e_time)

        print("[6] Enable & Save")
        enable_and_save(page)

        print("[DONE] 완료")
    finally:
        close(pw, browser, ctx)

if __name__ == "__main__":
    main()
