## VPN/방화벽 정책 자동화

신청ID, 사용기간(시작,종료 시각), 사무실PC IP를 입력받아, 외부 인증 서버/VPN 게이트웨이에 자동 로그인한 뒤 방화벽 정책에서 One-Time 스케줄을 생성하고 정책을 활성화(Enable)하는 자동화 웹앱

### Workflow
1. 사용자가 신청ID/기간/사무실IP 입력 → 요청 생성

2. 봇(자동화 에이전트)이 외부 인증 서버 로그인 → 신청ID 검색 → First Name이 VPN1인지 VPN2인지 판별

3. 판별 결과에 따라 VPN1 또는 VPN2 게이트웨이 URL로 로그인

4. 방화벽 관리(Policy & Objects → Firewall Policy) 에서 신청ID로 정책 검색 → Edit 진입

5. Source: 신청ID, EXT-User_Radius_GRP / Destination: 사무실PC IP

6. Schedule: Create → + One-Time Schedule (이름: YYYYMMDD_시작종료)

    예: 시작: 2025-07-01 07:00, 종료: 2025-07-01 22:00 → 20250701_0722

    (참고: Create 가이드 문서가 있다면 내부 링크 연결)

7. Enable this policy 체크 → OK 저장



