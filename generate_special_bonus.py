"""
삼성전자 DS부문 특별경영성과급 안내 페이지 (2026년 신설, 노조 투표 가결로 확정)

개인별 배분 공식이 공개되지 않았고 지급 자체가 3개년 누적 영업이익 조건부라
"연봉 입력 -> 내 몫 계산" 방식이 불가능함. 대신 조건 충족 시 회사 전체 재원 규모를
추정해보는 계산기 + 제도 설명으로 구성.
"""
import os
from static_pages import SITE_NAME, GA_SNIPPET, FOOTER_NAV, SITE_STYLE, SITE_HEADER, FAVICON

OUTPUT_DIR = "docs"

FUND_RATE = 0.105  # DS부문 영업이익의 10.5%
THRESHOLD_2628 = 200  # 2026~2028년 누적 영업이익 기준(조원)
THRESHOLD_2935 = 100  # 2029~2035년 누적 영업이익 기준(조원)

SOURCE_URL_AGREEMENT = "https://v.daum.net/v/ydg7YuHlvx"
SOURCE_URL_VOTE = "https://www.khan.co.kr/article/202605271027001"


def special_bonus_html():
    title = "삼성전자 DS부문 특별경영성과급 - 2026년 신설, 재원 규모 계산기"
    desc = "2026년 5월 노사 합의로 신설된 삼성전자 DS부문 특별경영성과급의 지급 조건과 예상 재원 규모를 확인하세요."

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
  <h1>삼성전자 DS부문 특별경영성과급</h1>
  <p>2026년 5월 노사가 새로 합의하고 노조 투표(찬성률 73.7%)로 확정된 제도입니다.
  기존 OPI·TAI와는 별도로 지급되며, DS부문 누적 영업이익이 일정 기준을 넘을 때만 발생합니다.</p>

  <div class="calc-box">
    <div class="field">
      <label for="profit">예상 DS부문 누적 영업이익 (조원, 2026~2028년 3개년 합계)</label>
      <input type="number" id="profit" placeholder="예: 250" oninput="calc()">
    </div>

    <div class="result">
      <div class="result-row"><span>지급 조건(누적 {THRESHOLD_2628}조원) 충족 여부</span><span id="eligible">-</span></div>
      <div class="result-row"><span>전체 재원 (영업이익의 {FUND_RATE * 100}%)</span><span id="fund">-</span></div>
      <div class="result-row"><span>├ 부문공통 배분 (40%)</span><span id="common">-</span></div>
      <div class="result-row total"><span>└ 사업부 배분 (60%)</span><span id="division">-</span></div>
    </div>
    <p class="stock-note">⚠ 이 결과는 <b>회사 전체 재원 규모 추정치</b>입니다. 정확한 개인별 배분 공식은
    공개되지 않았지만, 2026년 첫 지급분 기준 사업부별 1인당 평균 추정액은 아래 계산기에서 확인할 수
    있습니다.</p>
  </div>

  <div class="cross-link-box">
    📊 사업부별 특별경영성과급 + 기존 OPI·TAI까지 합산한 예상 총 성과급이 궁금하다면:
    <a href="samsung-ds-memory.html">메모리사업부</a> ·
    <a href="samsung-ds-systemlsi.html">시스템LSI</a> ·
    <a href="samsung-ds-foundry.html">파운드리</a> ·
    <a href="samsung-ds-common.html">DS 공통조직</a> 계산기
  </div>

  <h2>지급 조건</h2>
  <table class="rule">
    <tr><th>기간</th><th>누적 영업이익 기준</th></tr>
    <tr><td>2026~2028년 (3개년)</td><td class="num">{THRESHOLD_2628}조원 초과</td></tr>
    <tr><td>2029~2035년</td><td class="num">{THRESHOLD_2935}조원 (기간별 기준, 공개된 보도 기준)</td></tr>
  </table>
  <p class="source">2029~2035년 구간은 정확히 몇 년 단위로 끊어 재원을 산정하는지 공개 보도만으로는
  명확하지 않습니다. 정확한 산정 방식은 원 공시자료를 확인하세요.</p>

  <h2>제도 개요</h2>
  <ul>
    <li><b>재원</b>: DS부문 영업이익의 10.5% (기존 OPI와 별도)</li>
    <li><b>지급 방식</b>: 전액 자사주. 1/3은 즉시 매각 가능, 나머지는 일정 기간 매각 제한</li>
    <li><b>배분</b>: 부문공통 40% / 사업부 60%</li>
    <li><b>지급 한도</b>: 없음</li>
    <li><b>합의 유효기간</b>: 10년</li>
    <li><b>확정일</b>: 2026년 5월 27일 노조 찬반투표 가결(찬성률 73.7%)</li>
  </ul>

  <h2>출처</h2>
  <p class="source">
    <a href="{SOURCE_URL_AGREEMENT}" target="_blank" rel="noopener nofollow">노사 잠정합의 내용 보도</a> ·
    <a href="{SOURCE_URL_VOTE}" target="_blank" rel="noopener nofollow">노조 찬반투표 가결 보도</a>
  </p>

  <div class="disclaimer">
    ※ 이 페이지는 투자자문이 아닌 정보 제공용입니다. 특별경영성과급은 다년간 누적 실적에 좌우되는
    조건부 제도라 실제 지급 여부·시점·금액은 불확실합니다. 자사주로 지급되므로 실제 가치는 지급 시점
    주가에 따라 달라집니다. 개인별 배분 기준은 별도 사내 공지를 확인하세요.
  </div>
  {FOOTER_NAV}
  <script>
  const FUND_RATE = {FUND_RATE};
  const THRESHOLD = {THRESHOLD_2628};

  function calc() {{
    const profit = parseFloat(document.getElementById('profit').value) || 0;
    if (profit <= 0) return;

    const eligible = profit > THRESHOLD;
    document.getElementById('eligible').textContent = eligible ? '✅ 충족' : '❌ 미충족';

    if (!eligible) {{
      document.getElementById('fund').textContent = '0조원 (조건 미충족)';
      document.getElementById('common').textContent = '-';
      document.getElementById('division').textContent = '-';
      return;
    }}

    const fund = profit * FUND_RATE;
    const common = fund * 0.4;
    const division = fund * 0.6;

    document.getElementById('fund').textContent = fund.toFixed(1) + '조원';
    document.getElementById('common').textContent = common.toFixed(1) + '조원';
    document.getElementById('division').textContent = division.toFixed(1) + '조원';
  }}
  </script>
</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "samsung-special-bonus.html"), "w", encoding="utf-8") as f:
        f.write(special_bonus_html())
    print("삼성전자 특별경영성과급 페이지 생성 완료 -> docs/samsung-special-bonus.html")


if __name__ == "__main__":
    main()
