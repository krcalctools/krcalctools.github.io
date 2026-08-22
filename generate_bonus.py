"""
삼성전자 / SK하이닉스 성과급(OPI·TAI / PS·PI) 계산기 페이지 생성

개인 연봉/기본급은 알 수 없으므로 정적 값이 아니라 브라우저에서 입력받아
JS로 즉시 계산하는 방식(인터랙티브 계산기)으로 만든다.
기존 salary-*.html 과 같은 docs/ 폴더에 생성되어 한 사이트에 통합된다.
"""
import os
from static_pages import SITE_NAME, GA_SNIPPET, FOOTER_NAV, SITE_STYLE, SITE_HEADER, FAVICON
from bonus_data import (
    SAMSUNG_DIVISIONS, SAMSUNG_OPI_SOURCE, SAMSUNG_OPI_SOURCE_URL,
    SAMSUNG_TAI_H1_SOURCE, SAMSUNG_TAI_H1_SOURCE_URL,
    SPECIAL_BONUS_SOURCE, SPECIAL_BONUS_SOURCE_URL,
    SKHYNIX_PS_RATE, SKHYNIX_PS_SOURCE, SKHYNIX_PS_SOURCE_URL,
    SKHYNIX_PI_RATE_RECENT, SKHYNIX_PI_SOURCE, SKHYNIX_PI_SOURCE_URL,
)

OUTPUT_DIR = "docs"

FOOTER = FOOTER_NAV


def fmt(n):
    return f"{n:,}"


def samsung_page(div):
    opi_pct = round(div["opi_rate"] * 100)
    tai_pct = round(div["tai_h1_rate"] * 100)
    special_man = div["special_bonus_man"]
    special_eok = special_man / 10000
    title = f"삼성전자 {div['short']} 성과급 통합 계산기 - OPI·TAI·특별경영성과급 2026"
    desc = f"삼성전자 {div['name']}의 OPI·TAI·특별경영성과급까지 합산한 2026년 예상 총 성과급을 계산해보세요."

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
  <h1>삼성전자 {div['name']} 성과급 통합 계산기</h1>
  <p>OPI(초과이익성과급)·TAI(목표달성장려금)·특별경영성과급까지 전부 합산한 예상 총 성과급을 계산합니다.</p>

  <div class="calc-box">
    <div class="field">
      <label for="annual">연봉 (세전, 만원)</label>
      <input type="number" id="annual" placeholder="예: 6000" oninput="calc()">
    </div>
    <div class="field">
      <label for="monthly">월 기본급 (만원, 모르면 비워두면 연봉÷12로 추정)</label>
      <input type="number" id="monthly" placeholder="예: 400" oninput="calc()">
    </div>

    <div class="result">
      <div class="result-row"><span>OPI ({opi_pct}%, 연봉 기준)</span><span id="opi">-</span></div>
      <div class="result-row"><span>TAI 상반기 ({tai_pct}%, 월기본급 기준)</span><span id="tai">-</span></div>
      <div class="result-row"><span>TAI 하반기</span><span class="pending">12월 말 발표 예정 (미정)</span></div>
      <div class="result-row"><span>특별경영성과급 (2026년 첫 지급분, 1인당 추정)</span><span>{fmt(special_man)}만원 (약 {special_eok:g}억원)</span></div>
      <div class="result-row total"><span>예상 총 성과급 합계 (세전)</span><span id="total">-</span></div>
    </div>
    <p class="stock-note">※ 특별경영성과급은 연봉과 무관하게 보도된 1인당 평균 추정치를 그대로 더한 값입니다.
    {div['special_bonus_note']}</p>
  </div>

  <h2>계산 기준</h2>
  <p>OPI = 연봉 × {opi_pct}%<br>TAI(상반기) = 월 기본급 × {tai_pct}%<br>
  특별경영성과급 = 사업부 평균 추정치 {fmt(special_man)}만원 (연봉 무관 고정값)</p>
  <p class="source">OPI 지급률 출처: {SAMSUNG_OPI_SOURCE} — <a href="{SAMSUNG_OPI_SOURCE_URL}" target="_blank" rel="noopener nofollow">기사 보기</a></p>
  <p class="source">TAI 지급률 출처: {SAMSUNG_TAI_H1_SOURCE} — <a href="{SAMSUNG_TAI_H1_SOURCE_URL}" target="_blank" rel="noopener nofollow">기사 보기</a></p>
  <p class="source">특별경영성과급 출처: {SPECIAL_BONUS_SOURCE} — <a href="{SPECIAL_BONUS_SOURCE_URL}" target="_blank" rel="noopener nofollow">기사 보기</a>
  · <a href="samsung-special-bonus.html">제도 상세 설명 보기</a></p>

  <h2>OPI·TAI·특별경영성과급이란?</h2>
  <p><b>OPI(초과이익성과급, 구 PS)</b>는 사업부가 목표 이익을 초과 달성했을 때 연봉을 기준으로 연 1회(1월) 지급됩니다.
  <b>TAI(목표달성장려금, 구 PI)</b>는 사업부 목표 달성 여부에 따라 월 기본급을 기준으로 반기마다(7월·12월) 지급됩니다.
  <b>특별경영성과급</b>은 2026년 5월 신설된 DS부문 전용 제도로, 연봉과 무관하게 부문공통 균등배분 + 사업부 실적별
  추가배분으로 결정되며 전액 자사주로 지급됩니다.</p>

  <div class="disclaimer">
    ※ 세전 금액이며, 실제로는 상여소득세(OPI·TAI)와 자사주 평가차익 관련 세금(특별경영성과급)이 별도로
    발생합니다. OPI·TAI 지급률은 사업부 실적에 따라 매 반기·매년 달라지고, 특별경영성과급은 개인별
    배분 공식이 공개되지 않아 사업부 평균 추정치를 표시한 것으로 실제 개인 수령액과 다를 수 있습니다.
    최신 수치는 반드시 최근 뉴스로 다시 확인하세요.
  </div>
  {FOOTER}
  <script>
  const SPECIAL_MAN = {special_man};

  function calc() {{
    const annual = parseFloat(document.getElementById('annual').value) || 0;
    const monthlyInput = document.getElementById('monthly').value;
    const monthly = monthlyInput ? parseFloat(monthlyInput) : annual / 12;
    const opi = Math.round(annual * {div['opi_rate']});
    const tai = Math.round(monthly * {div['tai_h1_rate']});
    document.getElementById('opi').textContent = opi.toLocaleString() + '만원';
    document.getElementById('tai').textContent = tai.toLocaleString() + '만원';
    document.getElementById('total').textContent = (opi + tai + SPECIAL_MAN).toLocaleString() + '만원';
  }}
  </script>
</body>
</html>"""


def skhynix_page():
    ps_pct = round(SKHYNIX_PS_RATE * 100)
    pi_pct = round(SKHYNIX_PI_RATE_RECENT * 100)
    title = "SK하이닉스 성과급 계산기 - PS·PI 2026"
    desc = f"SK하이닉스 PS(초과이익분배금, 최근 {ps_pct}%)와 PI(생산성격려금, 최근 {pi_pct}%) 기준 예상 성과급을 계산해보세요."

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
  <h1>SK하이닉스 성과급 계산기</h1>
  <p>PS(초과이익분배금)와 PI(생산성격려금)를 최근 확정된 지급률 기준으로 계산합니다.</p>

  <div class="calc-box">
    <div class="field">
      <label for="annual">연봉 (세전, 만원)</label>
      <input type="number" id="annual" placeholder="예: 10000" oninput="calc()">
    </div>

    <div class="result">
      <div class="result-row"><span>PS (기준급 연봉÷20의 {ps_pct}%)</span><span id="ps">-</span></div>
      <div class="result-row"><span>PI 1회분 (월기본급의 {pi_pct}%, 연봉÷12로 추정)</span><span id="pi">-</span></div>
      <div class="result-row"><span>PI는 상·하반기 각각 지급 (2회분 = 위 금액×2, 매 반기 재확정)</span><span></span></div>
      <div class="result-row total"><span>PS + PI 1회분 합계 (세전)</span><span id="total">-</span></div>
    </div>
  </div>

  <h2>계산 기준</h2>
  <p>PS = (연봉 ÷ 20) × {ps_pct}%<br>PI = 월 기본급(≈연봉÷12) × {pi_pct}%</p>
  <p class="source">PS 지급률 출처: {SKHYNIX_PS_SOURCE} — <a href="{SKHYNIX_PS_SOURCE_URL}" target="_blank" rel="noopener nofollow">기사 보기</a></p>
  <p class="source">PI 지급률 출처: {SKHYNIX_PI_SOURCE} — <a href="{SKHYNIX_PI_SOURCE_URL}" target="_blank" rel="noopener nofollow">기사 보기</a></p>

  <h2>PS·PI란?</h2>
  <p><b>PS(초과이익분배금)</b>는 연간 영업이익의 일부를 재원으로 연 1회(2월) 지급되며, 상한이 폐지되어
  실적이 좋을수록 지급률이 크게 오를 수 있습니다. <b>PI(생산성격려금)</b>는 영업이익률 구간(0~150%)에 따라
  반기마다 지급되는 월 기본급 기준 인센티브입니다.</p>

  <div class="disclaimer">
    ※ 세전 금액이며, 실제로는 상여소득세가 별도로 공제됩니다. PS는 최근 합의로 현금 40%·자사주 60%로
    지급 구조가 바뀌는 중이라 실수령 현금은 표시 금액보다 적을 수 있습니다. PI 지급률은 매 반기 영업이익률에
    따라 0~150% 사이에서 달라지므로 최신 발표를 확인하세요.
  </div>
  {FOOTER}
  <script>
  function calc() {{
    const annual = parseFloat(document.getElementById('annual').value) || 0;
    const baseForPs = annual / 20;
    const monthly = annual / 12;
    const ps = Math.round(baseForPs * {SKHYNIX_PS_RATE});
    const pi = Math.round(monthly * {SKHYNIX_PI_RATE_RECENT});
    document.getElementById('ps').textContent = ps.toLocaleString() + '만원';
    document.getElementById('pi').textContent = pi.toLocaleString() + '만원';
    document.getElementById('total').textContent = (ps + pi).toLocaleString() + '만원';
  }}
  </script>
</body>
</html>"""


def bonus_index_html(pages):
    items = "\n".join(f'<li><a href="{p["file"]}">{p["label"]}</a></li>' for p in pages)
    return f"""<!doctype html>
<html lang="ko">
<head>
{GA_SNIPPET}
<meta charset="utf-8"><title>성과급 계산기 모음 - {SITE_NAME}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
{FAVICON}
<style>{SITE_STYLE}</style></head>
<body>
{SITE_HEADER}
<h1>대기업 성과급 계산기</h1>
<p>사업부/회사를 선택해서 연봉·기본급을 입력하면 예상 성과급을 바로 계산해드립니다.</p>
<ul class="division-list">{items}</ul>
{FOOTER}
</body></html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pages = []

    # SAMSUNG_DIVISIONS에서 빠진 사업부의 예전 페이지 정리 (특별경영성과급 안내 페이지는 별도 스크립트가 관리하므로 제외)
    valid_filenames = {f"samsung-{div['id']}.html" for div in SAMSUNG_DIVISIONS} | {"samsung-special-bonus.html"}
    for fname in os.listdir(OUTPUT_DIR):
        if fname.startswith("samsung-") and fname.endswith(".html") and fname not in valid_filenames:
            os.remove(os.path.join(OUTPUT_DIR, fname))

    for div in SAMSUNG_DIVISIONS:
        filename = f"samsung-{div['id']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(samsung_page(div))
        pages.append({"file": filename, "label": f"삼성전자 {div['name']} 성과급 계산기"})

    skhynix_filename = "skhynix.html"
    with open(os.path.join(OUTPUT_DIR, skhynix_filename), "w", encoding="utf-8") as f:
        f.write(skhynix_page())
    pages.append({"file": skhynix_filename, "label": "SK하이닉스 성과급 계산기"})

    pages.append({"file": "samsung-special-bonus.html", "label": "📌 삼성전자 DS부문 특별경영성과급 (2026년 신설)"})

    with open(os.path.join(OUTPUT_DIR, "bonus-index.html"), "w", encoding="utf-8") as f:
        f.write(bonus_index_html(pages))

    print(f"성과급 계산기 {len(pages)}개 페이지 + bonus-index.html 생성 완료 -> {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
