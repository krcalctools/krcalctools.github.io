"""
퇴직금 계산기 페이지 생성 (근로기준법 평균임금 기준, 인터랙티브 계산기)

법정 퇴직금 = 1일 평균임금 × 30일 × (재직일수 ÷ 365)
평균임금(1일) = 퇴직 전 3개월간 임금총액 ÷ 그 기간의 총 일수(약 90일)
(근로자퇴직급여 보장법 제8조, 근로기준법 제2조)
"""
import os
from static_pages import SITE_NAME, GA_SNIPPET, FOOTER_NAV

OUTPUT_DIR = "docs"

STYLE = """
  body { font-family: -apple-system, "Malgun Gothic", sans-serif; max-width: 640px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; line-height: 1.6; }
  h1 { font-size: 22px; }
  h2 { font-size: 16px; margin-top: 26px; }
  .calc-box { background: #f7f7fb; border-radius: 12px; padding: 20px; margin: 20px 0; }
  .field { margin-bottom: 14px; }
  .field label { display: block; font-size: 13px; color: #555; margin-bottom: 4px; }
  .field input { width: 100%; box-sizing: border-box; padding: 10px 12px; font-size: 16px; border: 1px solid #ddd; border-radius: 8px; }
  .result { margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e2ea; }
  .result-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 14px; }
  .result-row.total { font-weight: 700; font-size: 17px; color: #1958c9; border-top: 1px dashed #ccc; margin-top: 6px; padding-top: 10px; }
  .warning { margin-top: 12px; padding: 10px 12px; background: #fff4e5; border-radius: 8px; font-size: 13px; color: #92400e; display: none; }
  .source { font-size: 12px; color: #888; margin-top: 4px; }
  .source a { color: #888; }
  .disclaimer { margin-top: 30px; font-size: 12px; color: #999; line-height: 1.6; }
"""


def severance_html():
    title = "퇴직금 계산기 - 입사일·퇴사일로 즉시 계산"
    desc = "입사일, 퇴사일, 최근 3개월 급여만 입력하면 근로기준법 평균임금 기준 예상 퇴직금을 바로 계산해드립니다."

    return f"""<!doctype html>
<html lang="ko">
<head>
{GA_SNIPPET}
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{STYLE}</style>
</head>
<body>
  <h1>퇴직금 계산기</h1>
  <p>입사일과 퇴사일, 퇴직 전 3개월 평균 월급여를 입력하면 근로기준법 기준 예상 퇴직금을 계산합니다.</p>

  <div class="calc-box">
    <div class="field">
      <label for="startDate">입사일</label>
      <input type="date" id="startDate" oninput="calc()">
    </div>
    <div class="field">
      <label for="endDate">퇴사일 (예정일도 가능)</label>
      <input type="date" id="endDate" oninput="calc()">
    </div>
    <div class="field">
      <label for="monthly">퇴직 전 3개월 평균 월급여 (세전, 만원)</label>
      <input type="number" id="monthly" placeholder="예: 350" oninput="calc()">
    </div>

    <div class="warning" id="warning">
      ⚠ 재직기간이 1년 미만입니다. 근로자퇴직급여 보장법상 1년 미만 근속자는 법정 퇴직금 지급 의무가
      없습니다 (회사 자체 규정으로 지급하는 경우는 있을 수 있음).
    </div>

    <div class="result">
      <div class="result-row"><span>재직기간</span><span id="period">-</span></div>
      <div class="result-row"><span>1일 평균임금 (월급여×3÷90)</span><span id="avgwage">-</span></div>
      <div class="result-row total"><span>예상 퇴직금 (세전)</span><span id="total">-</span></div>
    </div>
  </div>

  <h2>계산 기준</h2>
  <p>퇴직금 = 1일 평균임금 × 30일 × (재직일수 ÷ 365)<br>
  1일 평균임금 = 퇴직 전 3개월 임금총액 ÷ 약 90일 (달력상 실제 일수 대신 단순화한 값)</p>
  <p class="source">법적 근거: 근로자퇴직급여 보장법 제8조, 근로기준법 제2조 — 정확한 산정은
  <a href="https://www.moel.go.kr/retirementpayCal.do" target="_blank" rel="noopener nofollow">고용노동부 퇴직금 계산기</a>에서
  실제 근무일수 기준으로 다시 확인하는 것을 권장합니다.</p>

  <h2>퇴직금이란?</h2>
  <p>계속근로기간 1년 이상인 근로자가 퇴직할 때 사용자가 지급해야 하는 법정 급여입니다. 4주 평균
  1주 소정근로시간이 15시간 이상이면 정규직·계약직·아르바이트 구분 없이 적용됩니다. 상여금, 연차수당
  중 일부가 평균임금 산정에 포함되는 경우도 있어 실제 금액은 이 계산기보다 높게 나올 수 있습니다.</p>

  <div class="disclaimer">
    ※ 세전 금액이며, 실제 지급 시 퇴직소득세가 별도로 원천징수됩니다. 평균임금은 실제 근무일수·상여금·
    연차수당 반영분에 따라 이 계산기의 단순화된 결과와 차이가 날 수 있습니다. 정확한 금액은 위 고용노동부
    계산기나 회사 인사팀을 통해 확인하세요.
  </div>
  {FOOTER_NAV}
  <script>
  function calc() {{
    const startVal = document.getElementById('startDate').value;
    const endVal = document.getElementById('endDate').value;
    const monthly = parseFloat(document.getElementById('monthly').value) || 0;
    if (!startVal || !endVal) return;

    const start = new Date(startVal);
    const end = new Date(endVal);
    const days = Math.round((end - start) / (1000 * 60 * 60 * 24));
    if (days <= 0) return;

    const years = Math.floor(days / 365);
    const remDays = days % 365;
    document.getElementById('period').textContent = years + '년 ' + remDays + '일 (총 ' + days.toLocaleString() + '일)';

    const avgWage = Math.round((monthly * 3 / 90) * 10000);
    const severance = Math.round(avgWage * 30 * (days / 365));

    document.getElementById('avgwage').textContent = avgWage.toLocaleString() + '원';
    document.getElementById('total').textContent = severance.toLocaleString() + '원';

    document.getElementById('warning').style.display = days < 365 ? 'block' : 'none';
  }}
  </script>
</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "severance.html"), "w", encoding="utf-8") as f:
        f.write(severance_html())
    print("퇴직금 계산기 페이지 생성 완료 -> docs/severance.html")


if __name__ == "__main__":
    main()
