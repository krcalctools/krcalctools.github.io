"""
연봉 실수령액 페이지 대량 생성 스크립트 (프로그래매틱 SEO 예시)

STEP/START/END 만 조절하면 페이지 수가 그대로 늘어난다.
각 페이지는 독립된 정적 HTML이라 호스팅 비용이 거의 안 들고(Vercel/Netlify 무료 티어),
검색엔진이 각각을 별도 URL로 색인한다.
"""
import os
from calc import calculate
from static_pages import about_html, privacy_html, contact_html, SITE_NAME, GA_SNIPPET, FOOTER_NAV

OUTPUT_DIR = "docs"  # GitHub Pages가 /docs 폴더를 바로 서빙할 수 있어서 이 이름 사용
BASE_URL = "https://krcalctools.github.io"

START = 20_000_000
END = 100_000_000
STEP = 1_000_000  # 100만원 단위. 실제 검색 패턴(딱 떨어지는 숫자)에 맞추고 유사페이지 과다생성을 피함


SALARY_CALC_JS = """
const PENSION_RATE = 0.045, PENSION_CAP = 6370000, PENSION_FLOOR = 370000;
const HEALTH_RATE = 0.03545, LTC_RATE_OF_HEALTH = 0.1295, EMPLOYMENT_RATE = 0.009;

function earnedIncomeDeduction(g) {
  if (g <= 5000000) return g * 0.7;
  if (g <= 15000000) return 3500000 + (g - 5000000) * 0.4;
  if (g <= 45000000) return 7500000 + (g - 15000000) * 0.15;
  if (g <= 100000000) return 12000000 + (g - 45000000) * 0.05;
  return 14750000 + (g - 100000000) * 0.02;
}

const TAX_BRACKETS = [
  [12000000, 0.06, 0], [46000000, 0.15, 1080000], [88000000, 0.24, 5220000],
  [150000000, 0.35, 14900000], [300000000, 0.38, 19400000], [500000000, 0.40, 25400000],
  [1000000000, 0.42, 35400000], [Infinity, 0.45, 65400000],
];

function taxByBracket(base) {
  if (base <= 0) return 0;
  for (const [limit, rate, deduction] of TAX_BRACKETS) {
    if (base <= limit) return base * rate - deduction;
  }
  return 0;
}

function earnedIncomeTaxCredit(tax, annual) {
  let credit = tax <= 1300000 ? tax * 0.55 : 715000 + (tax - 1300000) * 0.3;
  let cap;
  if (annual <= 33000000) cap = 740000;
  else if (annual <= 70000000) cap = Math.max(660000, 740000 - (annual - 33000000) * 0.008);
  else cap = Math.max(500000, 660000 - (annual - 70000000) * 0.5);
  return Math.min(credit, cap);
}

function calculateSalary(annual) {
  const monthly = annual / 12;
  const pensionBase = Math.min(Math.max(monthly, PENSION_FLOOR), PENSION_CAP);
  const pension = Math.round(pensionBase * PENSION_RATE);
  const health = Math.round(monthly * HEALTH_RATE);
  const ltc = Math.round(health * LTC_RATE_OF_HEALTH);
  const employment = Math.round(monthly * EMPLOYMENT_RATE);

  const deduction = earnedIncomeDeduction(annual);
  const earnedIncomeAmount = Math.max(annual - deduction, 0);
  const comprehensiveDeduction = 1500000 + pension * 12 + (health + ltc) * 12;
  const taxableBase = Math.max(earnedIncomeAmount - comprehensiveDeduction, 0);
  const calculatedTax = taxByBracket(taxableBase);
  const credit = earnedIncomeTaxCredit(calculatedTax, annual);
  const finalTaxAnnual = Math.max(calculatedTax - credit, 0);

  const incomeTax = Math.round(finalTaxAnnual / 12);
  const localTax = Math.round(incomeTax * 0.1);
  const totalDeduction = pension + health + ltc + employment + incomeTax + localTax;
  const netMonthly = Math.round(monthly - totalDeduction);

  return { pension, health, ltc, employment, incomeTax, localTax, netMonthly };
}

function calc() {
  const manInput = parseFloat(document.getElementById('annual').value) || 0;
  const annual = manInput * 10000;
  if (annual <= 0) return;
  const r = calculateSalary(annual);
  document.getElementById('pension').textContent = r.pension.toLocaleString() + '원';
  document.getElementById('health').textContent = r.health.toLocaleString() + '원';
  document.getElementById('ltc').textContent = r.ltc.toLocaleString() + '원';
  document.getElementById('employment').textContent = r.employment.toLocaleString() + '원';
  document.getElementById('tax').textContent = (r.incomeTax + r.localTax).toLocaleString() + '원';
  document.getElementById('net').textContent = r.netMonthly.toLocaleString() + '원';
}
"""


def fmt(n):
    return f"{n:,}"


def slug(salary):
    man = salary // 10_000
    return f"salary-{man}"


def page_html(salary, prev_salary, next_salary):
    r = calculate(salary)
    man = salary // 10_000
    title = f"연봉 {fmt(man)}만원 실수령액 - 월 {fmt(r['net_monthly'])}원 (2025년 기준)"
    desc = f"연봉 {fmt(man)}만원의 세후 실수령액은 월 약 {fmt(r['net_monthly'])}원입니다. 4대보험, 소득세 공제 내역을 확인하세요."

    nav_links = []
    if prev_salary:
        nav_links.append(f'<a href="{slug(prev_salary)}.html">← 연봉 {prev_salary//10_000:,}만원</a>')
    if next_salary:
        nav_links.append(f'<a href="{slug(next_salary)}.html">연봉 {next_salary//10_000:,}만원 →</a>')
    nav_html = " | ".join(nav_links)

    return f"""<!doctype html>
<html lang="ko">
<head>
{GA_SNIPPET}
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: -apple-system, "Malgun Gothic", sans-serif; max-width: 640px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; }}
  h1 {{ font-size: 22px; }}
  .headline {{ background: #f0f6ff; border-radius: 12px; padding: 24px; text-align: center; margin: 20px 0; }}
  .headline .amount {{ font-size: 34px; font-weight: 800; color: #1958c9; }}
  table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
  th, td {{ text-align: left; padding: 10px 8px; border-bottom: 1px solid #eee; font-size: 14px; }}
  th {{ color: #666; font-weight: 500; }}
  .nav {{ margin-top: 30px; font-size: 14px; }}
  .explain {{ margin-top: 28px; font-size: 14px; color: #444; }}
  .explain h2 {{ font-size: 15px; }}
  .steps {{ margin: 12px 0 0; padding-left: 20px; }}
  .steps li {{ margin-bottom: 8px; }}
  .steps .num {{ color: #1958c9; font-weight: 600; }}
  .disclaimer {{ margin-top: 40px; font-size: 12px; color: #999; line-height: 1.6; }}
  .footer-nav {{ margin-top: 24px; padding-top: 16px; border-top: 1px solid #eee; font-size: 13px; }}
  .footer-nav a {{ color: #666; margin-right: 12px; }}
</style>
</head>
<body>
  <h1>연봉 {fmt(man)}만원 실수령액 계산 결과</h1>
  <div class="headline">
    <div>세전 연봉 {fmt(man)}만원의 월 실수령액</div>
    <div class="amount">{fmt(r['net_monthly'])}원</div>
    <div>연 실수령액 약 {fmt(r['net_annual'])}원</div>
  </div>

  <table>
    <tr><th>항목</th><th>월 공제액</th></tr>
    <tr><td>국민연금</td><td>{fmt(r['pension'])}원</td></tr>
    <tr><td>건강보험</td><td>{fmt(r['health'])}원</td></tr>
    <tr><td>장기요양보험</td><td>{fmt(r['longterm_care'])}원</td></tr>
    <tr><td>고용보험</td><td>{fmt(r['employment'])}원</td></tr>
    <tr><td>소득세</td><td>{fmt(r['income_tax'])}원</td></tr>
    <tr><td>지방소득세</td><td>{fmt(r['local_tax'])}원</td></tr>
    <tr><th>공제 합계</th><th>{fmt(r['total_deduction'])}원</th></tr>
  </table>

  <div class="nav">{nav_html}</div>

  <div class="explain">
    <h2>연봉 {fmt(man)}만원의 실수령액 계산 과정</h2>
    <ol class="steps">
      <li>월 급여 = 연봉 {fmt(man)}만원 ÷ 12 = <span class="num">{fmt(r['gross_monthly'])}원</span></li>
      <li>4대보험 공제(월) = 국민연금 {fmt(r['pension'])}원 + 건강보험 {fmt(r['health'])}원
        + 장기요양보험 {fmt(r['longterm_care'])}원 + 고용보험 {fmt(r['employment'])}원
        = <span class="num">{fmt(r['pension'] + r['health'] + r['longterm_care'] + r['employment'])}원</span></li>
      <li>근로소득공제(연) = <span class="num">{fmt(r['earned_income_deduction'])}원</span>을 연봉에서 제외 →
        근로소득금액 <span class="num">{fmt(r['earned_income_amount'])}원</span></li>
      <li>종합소득공제(연) = 기본공제 150만원 + 국민연금 납부액(연) + 건강보험료 납부액(연)
        = <span class="num">{fmt(r['comprehensive_deduction'])}원</span></li>
      <li>과세표준 = 근로소득금액 − 종합소득공제 = <span class="num">{fmt(r['taxable_base'])}원</span></li>
      <li>산출세액(연) = 과세표준에 누진세율 적용 = <span class="num">{fmt(r['calculated_tax_annual'])}원</span></li>
      <li>근로소득세액공제(연) = <span class="num">{fmt(r['tax_credit_annual'])}원</span> 차감 →
        결정세액(연) <span class="num">{fmt(r['final_tax_annual'])}원</span> → 월 소득세
        <span class="num">{fmt(r['income_tax'])}원</span> (+지방소득세 {fmt(r['local_tax'])}원)</li>
      <li>실수령액 = 월급여 − 4대보험 − 소득세 − 지방소득세 = <span class="num">{fmt(r['net_monthly'])}원</span></li>
    </ol>
  </div>

  <div class="explain">
    <h2>공제 항목 설명</h2>
    <p>국민연금은 표준 소득월액의 4.5%를 근로자가 부담하며, 상한액과 하한액이 매년 조정됩니다.
    건강보험은 소득의 3.545%, 여기에 건강보험료의 12.95%가 장기요양보험료로 추가 부과됩니다.
    고용보험은 소득의 0.9%이며, 소득세와 지방소득세는 연간 근로소득을 기준으로 누진세율이
    적용된 뒤 12개월로 나눈 값입니다. 부양가족이 있거나 각종 세액공제 대상이라면 실제 공제액은
    이 표보다 낮아질 수 있습니다.</p>
  </div>

  <div class="disclaimer">
    ※ 본 계산은 1인 가구 기준으로 기본공제·연금보험료공제·건강보험료 특별소득공제를 반영한
    추정치입니다. 부양가족 공제, 카드사용액 등 그 외 소득·세액공제, 비과세 수당 등은 반영하지
    않아 실제 금액과 차이가 있을 수 있습니다. 4대보험 요율은 2025년 예시 기준이며 매년 변경되므로
    정확한 금액은 국세청 홈택스 원천징수세액 조회를 참고하세요.
  </div>

{FOOTER_NAV}
</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    salaries = list(range(START, END + 1, STEP))

    # START/END/STEP이 바뀌면 예전 값으로 만들어진 salary-*.html이 남을 수 있어 먼저 정리
    valid_filenames = {f"{slug(s)}.html" for s in salaries}
    for fname in os.listdir(OUTPUT_DIR):
        if fname.startswith("salary-") and fname.endswith(".html") and fname not in valid_filenames:
            os.remove(os.path.join(OUTPUT_DIR, fname))

    urls = []
    for i, salary in enumerate(salaries):
        prev_s = salaries[i - 1] if i > 0 else None
        next_s = salaries[i + 1] if i < len(salaries) - 1 else None
        html = page_html(salary, prev_s, next_s)
        path = os.path.join(OUTPUT_DIR, f"{slug(salary)}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        urls.append(f"{BASE_URL}/{slug(salary)}.html")

    # 필수 정적 페이지 (애드센스 심사용)
    static_files = {"about.html": about_html(), "privacy.html": privacy_html(), "contact.html": contact_html()}
    for filename, html in static_files.items():
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html)
        urls.append(f"{BASE_URL}/{filename}")

    # index.html - 전체 목록
    links = "\n".join(
        f'<li><a href="{slug(s)}.html">연봉 {s//10_000:,}만원 실수령액</a></li>' for s in salaries
    )
    index_html = f"""<!doctype html>
<html lang="ko"><head>
{GA_SNIPPET}
<meta charset="utf-8"><title>{SITE_NAME} - 연봉별 실수령액 계산 결과</title>
<meta name="google-site-verification" content="22jd1Q9gwpfGcwd0MvSlxlhC8mekAJ9CjNMXHGUHASE" />
<meta name="naver-site-verification" content="2619bf9b6ab4ed06c679f8f24d5b50df019827ac" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: -apple-system, "Malgun Gothic", sans-serif; max-width: 640px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; }}
  .calc-box {{ background: #f7f7fb; border-radius: 12px; padding: 20px; margin: 20px 0; }}
  .field {{ margin-bottom: 14px; }}
  .field label {{ display: block; font-size: 13px; color: #555; margin-bottom: 4px; }}
  .field input {{ width: 100%; box-sizing: border-box; padding: 10px 12px; font-size: 16px; border: 1px solid #ddd; border-radius: 8px; }}
  .result {{ margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e2ea; }}
  .result-row {{ display: flex; justify-content: space-between; padding: 6px 0; font-size: 14px; }}
  .result-row.total {{ font-weight: 700; font-size: 17px; color: #1958c9; border-top: 1px dashed #ccc; margin-top: 6px; padding-top: 10px; }}
  .footer-nav {{ margin-top: 24px; padding-top: 16px; border-top: 1px solid #eee; font-size: 13px; }}
  .footer-nav a {{ color: #666; margin-right: 12px; }}
</style></head>
<body>
<h1>연봉 실수령액 계산기</h1>
<p>정확한 연봉을 입력하면 바로 계산됩니다. 아래 목록은 자주 찾는 연봉 구간별 상세 계산 결과입니다.</p>

<div class="calc-box">
  <div class="field">
    <label for="annual">연봉 (세전, 만원)</label>
    <input type="number" id="annual" placeholder="예: 3637" oninput="calc()">
  </div>
  <div class="result">
    <div class="result-row"><span>국민연금</span><span id="pension">-</span></div>
    <div class="result-row"><span>건강보험</span><span id="health">-</span></div>
    <div class="result-row"><span>장기요양보험</span><span id="ltc">-</span></div>
    <div class="result-row"><span>고용보험</span><span id="employment">-</span></div>
    <div class="result-row"><span>소득세+지방소득세</span><span id="tax">-</span></div>
    <div class="result-row total"><span>월 실수령액</span><span id="net">-</span></div>
  </div>
</div>

<p><a href="bonus-index.html"><b>삼성전자·SK하이닉스 성과급 계산기</b></a> | <a href="severance.html"><b>퇴직금 계산기</b></a> | <a href="unemployment.html"><b>실업급여 계산기</b></a> | <a href="dividend.html"><b>배당금 계산기</b></a></p>
<h2>연봉 구간별 상세 계산 결과 ({len(salaries)}개)</h2>
<ul>{links}</ul>
{FOOTER_NAV}
<script>
{SALARY_CALC_JS}
</script>
</body></html>"""
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # sitemap.xml
    sitemap_entries = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}
</urlset>"""
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    print(f"생성 완료: {len(salaries)}개 페이지 + index.html + sitemap.xml -> {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
