"""
근로소득자 연봉 백분위(상위 몇 %) 추정 테이블

방법론: 국세청 근로소득 백분위(천분위) 자료 중
- 2024년 귀속 자료(2025-12-31 등록, 가장 최근 공개분)의 확정 앵커 포인트(상위 50/30/10/1%)에
- 2021년 귀속 자료의 전체 분포 곡선(0.1~90% 전 구간)을 성장률로 스케일링해 나머지 구간을 보간함.
검증: 스케일링 후 앵커 포인트(50/30/10/1%)에서 오차가 원 자료와 거의 0으로 일치해 보간 신뢰도가 높음.

주의: 0.1~10%, 20~90% 구간은 보간 추정치이며, 국세청이 매년 12월 말 새 자료를 공개하므로
그때마다 앵커 포인트(가능하면 전체 구간)를 최신 자료로 갱신할 것.

출처:
- 2024년 귀속 앵커(50/30/10/1%): https://income.worldtourlist.com/ (국세청 근로소득 백분위 자료 인용)
- 2021년 귀속 전체 분포 곡선: https://intoday.kr/1147 (국세청 자료 인용)
"""

# (상위 퍼센트, 연봉 만원) - 퍼센트 오름차순(상위 0.1%가 가장 소득 높음)
PERCENTILE_TABLE = [
    (0.1, 104300),
    (1, 19950),
    (5, 11870),
    (10, 9120),
    (20, 6580),
    (30, 5060),
    (40, 4120),
    (50, 3420),
    (60, 2850),
    (70, 2420),
    (80, 1620),
    (90, 790),
]

SOURCE_NOTE = "2024년 귀속 국세청 근로소득 백분위 자료 기준(주요 구간 실측, 나머지는 2021년 분포 형태로 보간)"


def estimate_top_percent(annual_man_won: float) -> float:
    """연봉(만원)을 받아 대략적인 '상위 몇 %'를 반환. 표 범위 밖이면 양 끝값으로 고정."""
    table = PERCENTILE_TABLE
    if annual_man_won >= table[0][1]:
        return table[0][0]
    if annual_man_won <= table[-1][1]:
        return table[-1][0]

    for i in range(len(table) - 1):
        p_hi, v_hi = table[i]
        p_lo, v_lo = table[i + 1]
        if v_lo <= annual_man_won <= v_hi:
            # 구간 내 선형 보간 (연봉 기준으로 퍼센트를 보간)
            ratio = (annual_man_won - v_lo) / (v_hi - v_lo)
            return round(p_lo - ratio * (p_lo - p_hi), 1)
    return 90.0


if __name__ == "__main__":
    for salary_man in [2500, 3420, 5000, 6580, 10000, 20000]:
        print(f"연봉 {salary_man:,}만원 -> 상위 {estimate_top_percent(salary_man)}%")
