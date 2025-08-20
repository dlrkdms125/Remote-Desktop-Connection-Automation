# 로그인 폼
# --- 인증 서버 ---
AUTH_LOGIN_USER = ["#id_username", "input[name='username']"]
AUTH_LOGIN_PASS = ["#id_password", "input[name='password']"]
AUTH_LOGIN_SUBMIT = ["input[type='submit']", "button[type='submit']"]

# --- VPN ---
VPN_LOGIN_USER = ["#username", "input[name='username']"]
VPN_LOGIN_PASS = ["#secretkey", "input[name='secretkey']"]
VPN_LOGIN_SUBMIT = [
    "#login_button",           # 정확히 VPN1 버튼 id
    "button[name='login_button']",
    "button.primary",          # class로 fallback
    "button:has-text('Login')" # 텍스트로 fallback
]
# 인증 서버 내 네비게이션
NAV_AUTH       = "Authentication"
NAV_USER_MGMT  = "User Management"
NAV_LOCAL_USERS= "Local Users"
# FortiAuthenticator 우측 상단 검색창
LOCAL_USERS_SEARCH = [
    "input[placeholder='Search for local users']",
    "input[placeholder*='Search']",
    "input[type='search']"
]
ROW_FIRST_NAME_CELL = "td:nth-child(3)"  # First Name 컬럼 위치에 맞게 필요시 변경

# VPN/Firewall 메뉴
MENU_POLICY   = "Policy & Objects"
MENU_FIREWALL = "Firewall Policy"
FIREWALL_SEARCH = ["input[placeholder*='Search']", "input[type='search']"]

# 정책 편집 폼
FIELD_SOURCE_INPUT = "[aria-label='Source'] input, [data-field='source'] input"      
FIELD_DEST_INPUT   = "[aria-label='Destination'] input, [data-field='destination'] input"
SCHEDULE_DROPDOWN  = "[aria-label='Schedule'] .dropdown-toggle, [data-field='schedule'] .dropdown-toggle"
BTN_CREATE         = "text=Create"
BTN_ONE_TIME       = "text=One-Time Schedule, text=One Time"

DIALOG_NAME        = "input[name='name'], input[aria-label='Name']"
DIALOG_START_DATE  = "input[name='start_date'], input[aria-label='Start Date']"
DIALOG_START_TIME  = "input[name='start_time'], input[aria-label='Start Time']"
DIALOG_END_DATE    = "input[name='end_date'], input[aria-label='End Date']"
DIALOG_END_TIME    = "input[name='end_time'], input[aria-label='End Time']"
DIALOG_OK          = "button:has-text('OK')"

POLICY_ENABLE      = "label:has-text('Enable this policy'), [aria-label='Enable this policy']"
POLICY_OK          = "button:has-text('OK')"
