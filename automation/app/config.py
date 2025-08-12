import os
from dotenv import load_dotenv


load_dotenv()

AUTH_URL=os.getenv("AUTH_URL")
AUTH_USER=os.getenv("AUTH_USER")
AUTH_PASS=os.getenv("AUTH_PASS")

VPN1_URL=os.getenv("VPN1_URL")
VPN2_URL=os.getenv("VPN2_URL")
VPN_USER=os.getenv("VPN_USER")
VPN_PASS=os.getenv("VPN_PASS")

def build_schedule_name(start_str: str, end_str: str) -> str:
    return f"{start_str[:8]}_{start_str[-2:]}{end_str[-2:]}"

def split_date_time(dt_str: str):
    date = f"{dt_str[:4]}-{dt_str[4:6]}-{dt_str[6:8]}"
    time = f"{int(dt_str[-2:]):02d}:00"
    return date, time