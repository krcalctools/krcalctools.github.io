"""
배당금 계산기 페이지 생성 (종목 선택 기반, 인터랙티브)

투자자문이 아닌 정보 제공 목적: 배당금(DPS)은 공시된 확정 사실만 사용하고,
배당수익률은 사용자가 직접 입력한 매수단가로 계산한다(임의의 현재 주가를 단정하지 않음).
"""
import os
import json
from static_pages import SITE_NAME, GA_SNIPPET, FOOTER_NAV, SITE_STYLE, SITE_HEADER, FAVICON
from dividend_data import STOCKS

OUTPUT_DIR = "docs"


def dividend_html():
    title = "배당금 계산기 - 삼성전자·4대금융지주·SK텔레콤·KT&G"
    desc = "보유 주식 수를 입력하면 2025년 확정 배당금 기준 세후 배당 실수령액을 계산해드립니다."

    options = "\n".join(
        f'<option value="{s["id"]}">{s["name"]} (연 {s["dps"]:,}원/주)</option>' for s in STOCKS
    )
    stock_data_json = json.dumps({s["id"]: {"name": s["name"], "dps": s["dps"]} for s in STOCKS}, ensure_ascii=False)

    table_rows = "\n".join(
        f'<tr><td>{s["name"]}</td><td class="num">{s["dps"]:,}원</td>'
        f'<td class="source"><a href="{s["source_url"]}" target="_blank" rel="noopener nofollow">출처</a></td></tr>'
        for s in STOCKS
    )
    notes = "\n".join(f'<li><b>{s["name"]}</b>: {s["note"]}</li>' for s in STOCKS)

    return f"""<!doctype html>
<html lang="ko">
<head>
{GA_SNIPPET}
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="viewport" content="width=device-width, initial-scale=1">
{FAVICON}
<style>{SITE_STYLE}</style>
</head>
<body>
{SITE_HEADER}
  <h1>배당금 계산기</h1>
  <p>종목과 보유 주식 수를 입력하면 2025년 확정 배당금(DPS) 기준 세전/세후 배당금을 계산합니다.</p>

  <div class="calc-box">
    <div class="field">
      <label for="stock">종목 선택</label>
      <select id="stock" onchange="calc()">
        {options}
      </select>
    </div>
    <div class="field">
      <label for="shares">보유 주식 수</label>
      <input type="number" id="shares" placeholder="예: 100" oninput="calc()">
    </div>
    <div class="field">
      <label for="price">매수단가 (원, 배당수익률 계산용 · 선택)</label>
      <input type="number" id="price" placeholder="예: 85000" oninput="calc()">
    </div>

    <div class="result">
      <div class="result-row"><span>연간 세전 배당금</span><span id="gross">-</span></div>
      <div class="result-row"><span>배당소득세 (15.4%)</span><span id="tax">-</span></div>
      <div class="result-row total"><span>연간 세후 실수령 배당금</span><span id="net">-</span></div>
      <div class="result-row"><span>배당수익률 (매수단가 입력 시)</span><span id="yield">-</span></div>
    </div>
    <div class="stock-note" id="note"></div>
  </div>

  <h2>2025년 확정 연간 배당금(DPS) 비교</h2>
  <table class="rule">
    <tr><th>종목</th><th>연간 배당금(주당)</th><th>출처</th></tr>
    {table_rows}
  </table>
  <p class="source" style="margin-top:8px">최근 보도에서는 4대 금융지주 중 우리금융지주(배당수익률 6%대 후반)·하나금융지주(5%대 중후반)가
  상대적으로 높은 배당수익률로, 삼성전자는 배당수익률 자체는 낮은 대신 자사주 매입·소각 등 다른 주주환원 방식
  비중이 큰 것으로 보도되었습니다. 배당수익률은 주가에 따라 매일 바뀌므로 정확한 값은 매수 시점에 직접 확인하세요.</p>

  <h2>종목별 참고사항</h2>
  <ul>{notes}</ul>

  <h2>배당소득세는 왜 15.4%인가</h2>
  <p>국내 상장주식 배당소득에는 소득세 14% + 지방소득세 1.4%가 원천징수됩니다. 단, 금융소득(이자+배당)이
  연 2,000만원을 넘으면 다른 소득과 합산해 종합과세되어 세율이 달라질 수 있습니다.</p>

  <div class="disclaimer">
    ※ 본 계산기는 투자자문이나 특정 종목 매수 추천이 아닌 정보 제공용 도구입니다. 배당금은 매년 이사회
    결의로 증액·감액·중단될 수 있으며 과거 배당이 미래 배당을 보장하지 않습니다. 배당수익률이 비정상적으로
    높게 보이는 경우 주가 급락에 따른 "고배당의 함정"일 수 있으니 배당성향·실적 추이를 함께 확인하세요.
    최신 공시는 <a href="https://dart.fss.or.kr" target="_blank" rel="noopener nofollow">DART 전자공시시스템</a>에서
    확인할 수 있습니다.
  </div>
  {FOOTER_NAV}
  <script>
  const STOCKS = {stock_data_json};

  function calc() {{
    const stockId = document.getElementById('stock').value;
    const shares = parseFloat(document.getElementById('shares').value) || 0;
    const price = parseFloat(document.getElementById('price').value) || 0;
    const stock = STOCKS[stockId];
    if (!stock || shares <= 0) return;

    const gross = stock.dps * shares;
    const tax = Math.round(gross * 0.154);
    const net = gross - tax;

    document.getElementById('gross').textContent = gross.toLocaleString() + '원';
    document.getElementById('tax').textContent = tax.toLocaleString() + '원';
    document.getElementById('net').textContent = net.toLocaleString() + '원';

    if (price > 0) {{
      const yieldPct = (stock.dps / price * 100).toFixed(2);
      document.getElementById('yield').textContent = yieldPct + '%';
    }} else {{
      document.getElementById('yield').textContent = '매수단가 입력 필요';
    }}
  }}
  window.onload = calc;
  </script>
</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "dividend.html"), "w", encoding="utf-8") as f:
        f.write(dividend_html())
    print("배당금 계산기 페이지 생성 완료 -> docs/dividend.html")


if __name__ == "__main__":
    main()
