"""
배당금 계산기 데이터 - 2025년 확정(실제 지급/공시된) 연간 주당배당금(DPS) 기준
뉴스/공시 검색 기반, 2026-08-22 조사. 배당금은 매년 이사회 결정으로 바뀌므로
다음 결산 시즌(통상 1~2월)마다 최신 공시로 갱신 필요.

배당수익률(yield)은 아래 price/price_date 기준 스냅샷으로 계산한 값이며,
주가가 매일 바뀌므로 시간이 지나면 부정확해짐 -> 주기적으로 price/price_date 갱신 필요.
계산기 자체는 사용자가 직접 매수단가를 입력하면 본인 기준 수익률도 별도 계산해줌.
"""

PRICE_DATE = "2026-08-21"

STOCKS = [
    {
        "id": "samsung",
        "name": "삼성전자",
        "dps": 1668,
        "price": 281500,
        "note": "2025년 4분기 특별배당(5년 만) 포함. 특별배당은 매년 반복되지 않을 수 있음. AI/HBM 수요로 주가가 급등해 배당수익률은 낮은 편",
        "source_url": "https://www.thelec.kr/news/articleView.html?idxno=51546",
    },
    {
        "id": "ktng",
        "name": "KT&G",
        "dps": 4600,
        "price": 172300,
        "note": "2025년 결산배당 기준. 최근 5년간 매년 증가 추세",
        "source_url": "https://en.ktng.com/ir/stock-info/dividend",
    },
    {
        "id": "sktelecom",
        "name": "SK텔레콤",
        "dps": 2710,
        "price": 102200,
        "note": "2025년 4분기 결산배당은 실적 변동으로 미실시되어 예년보다 총액이 낮음",
        "source_url": "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20250212800008",
    },
    {
        "id": "kbfinancial",
        "name": "KB금융",
        "dps": 4367,
        "price": 164300,
        "note": "2025년 4분기 DPS 1,605원 포함 연간 확정치",
        "source_url": "https://zdnet.co.kr/view/?no=20260205141805",
    },
    {
        "id": "shinhan",
        "name": "신한지주",
        "dps": 2590,
        "price": 104100,
        "note": "2025년 연간 확정, 주주환원율 사상 첫 50% 돌파",
        "source_url": "https://news.nate.com/view/20260205n22140",
    },
    {
        "id": "hana",
        "name": "하나금융지주",
        "dps": 4105,
        "price": 128800,
        "note": "전년 대비 14.0%(505원) 증가, 사상 첫 순이익 4조 클럽",
        "source_url": "https://www.etoday.co.kr/news/view/2551435",
    },
    {
        "id": "woori",
        "name": "우리금융지주",
        "dps": 1360,
        "price": 31750,
        "note": "현금배당성향 첫 30% 상회. 배당 발표 시점보다 주가가 크게 올라 수익률이 낮아짐",
        "source_url": "https://www.thevaluenews.co.kr/news/196849",
    },
]

for _s in STOCKS:
    _s["yield_pct"] = round(_s["dps"] / _s["price"] * 100, 2)
