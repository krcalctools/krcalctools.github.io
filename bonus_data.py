"""
삼성전자·SK하이닉스 성과급 계산기 데이터 (뉴스 검색 기반, 2026-08-22 기준)

주의: 아래 지급률은 특정 시점에 확정/보도된 값이며 반기/연 단위로 계속 바뀝니다.
실배포 후에도 주기적으로 최신 뉴스를 검색해서 갱신해야 합니다.
"""

# 삼성전자 OPI(초과이익성과급, 구 PS) - 연봉 기준, 연 1회(1월) 지급
# 2025년 실적 기준, 2026년 1월 확정
SAMSUNG_OPI_SOURCE = "2025년 귀속 실적 기준 (2026년 1월 확정, 1월 말 지급)"
SAMSUNG_OPI_SOURCE_URL = "https://dealsite.co.kr/articles/155212"

# 삼성전자 TAI(목표달성장려금, 구 PI) - 월 기본급 기준, 반기별(7월/12월) 지급
SAMSUNG_TAI_H1_SOURCE = "2026년 상반기 확정 (2026년 7월 8일 지급). 하반기는 12월 말 별도 발표 예정으로 아직 미정"
SAMSUNG_TAI_H1_SOURCE_URL = "https://zdnet.co.kr/view/?no=20260706154914"

SAMSUNG_DIVISIONS = [
    {
        "id": "ds-memory",
        "name": "DS부문 - 메모리사업부",
        "short": "메모리(반도체)",
        "opi_rate": 0.47,
        "tai_h1_rate": 1.00,
    },
    {
        "id": "ds-systemlsi-foundry",
        "name": "DS부문 - 시스템LSI·파운드리",
        "short": "시스템LSI·파운드리",
        "opi_rate": 0.47,
        "tai_h1_rate": 0.75,
    },
]

# SK하이닉스 PS(초과이익분배금) - 기준급(연봉÷20) 기준, 연 1회(2월) 지급
SKHYNIX_PS_RATE = 29.64  # 2964%, 2025년 실적 기준, 2026년 2월 지급
SKHYNIX_PS_SOURCE = "2025년 실적 기준 (2026년 2월 지급 완료)"
SKHYNIX_PS_SOURCE_URL = "https://www.busan.com/view/busan/view.php?code=2026020417284483907"

# SK하이닉스 PI(생산성격려금) - 월 기본급 기준, 반기별(상/하반기) 지급, 영업이익률에 따라 0~150%
SKHYNIX_PI_RATE_RECENT = 1.50  # 150%, 최근 확정 회차(2025년 하반기분, 2026년 1월 지급) 기준
SKHYNIX_PI_SOURCE = "최근 확정 회차(2025년 하반기분, 2026년 1월 지급) 기준. 실제 지급률은 영업이익률 구간에 따라 0~150% 사이에서 매 반기 결정됨"
SKHYNIX_PI_SOURCE_URL = "https://www.hankyung.com/article/202407257752Y"
