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

# 특별경영성과급 - 2026년 5월 신설, 사업부별 1인당 추정 수령액(2026년 첫 지급분, 자사주 기준)
# 균등배분(부문공통 40%, 전원 1.6억) + 사업부 추가배분(60%, 메모리:공통조직=1:0.7, 적자예상 사업부는 추가분 없음)
SPECIAL_BONUS_SOURCE = "2026년 5월 노사 잠정합의·노조 투표 가결(찬성률 73.7%) 기준 보도된 1인당 추정 수령액"
SPECIAL_BONUS_SOURCE_URL = "https://www.hankyung.com/amp/2026052102857"

SAMSUNG_DIVISIONS = [
    {
        "id": "ds-memory",
        "name": "DS부문 - 메모리사업부",
        "short": "메모리(반도체)",
        "opi_rate": 0.47,
        "tai_h1_rate": 1.00,
        "special_bonus_man": 60000,  # 6억원 (기본 1.6억 + 사업부 추가분 약 3.8~4.4억, 언론사별 5.4~6억으로 편차)
        "special_bonus_note": "기본 배분 1.6억원 + 메모리사업부 추가배분. 언론사별로 5.4억~6억원까지 편차 있음",
    },
    {
        "id": "ds-systemlsi",
        "name": "DS부문 - 시스템LSI사업부",
        "short": "시스템LSI",
        "opi_rate": 0.47,
        "tai_h1_rate": 0.75,
        "special_bonus_man": 16000,  # 1.6억원 (최소 보장, 2026년 적자 예상으로 사업부 추가배분 없음)
        "special_bonus_note": "2026년 적자 예상으로 기본 배분(1.6억원)만 보장. 시스템LSI·파운드리는 별도 수치가 보도되지 않아 동일하게 적용",
    },
    {
        "id": "ds-foundry",
        "name": "DS부문 - 파운드리사업부",
        "short": "파운드리",
        "opi_rate": 0.47,
        "tai_h1_rate": 0.75,
        "special_bonus_man": 16000,  # 1.6억원 (최소 보장, 시스템LSI와 동일 취급)
        "special_bonus_note": "2026년 적자 예상으로 기본 배분(1.6억원)만 보장. 시스템LSI·파운드리는 별도 수치가 보도되지 않아 동일하게 적용",
    },
    {
        "id": "ds-common",
        "name": "DS부문 공통(지원조직)",
        "short": "DS 공통조직",
        "opi_rate": 0.47,
        "tai_h1_rate": 1.00,
        "special_bonus_man": 43000,  # 4.3억원 (기본 1.6억 + 공통조직 추가배분 약 2.7억)
        "special_bonus_note": "기본 배분 1.6억원 + 공통조직 추가배분(메모리 대비 0.7배 비율) 약 2.7억원",
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
