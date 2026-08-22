"""
애드센스 심사에 필요한 필수 정적 페이지 (개인정보처리방침 / 사이트소개 / 문의)
"""

SITE_NAME = "연봉실수령액계산기"
CONTACT_EMAIL = "contact@yourdomain.com"  # 실배포 전 실제 연락처 이메일로 교체하세요

GA_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HKGC6LX6C4"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-HKGC6LX6C4');
</script>"""

FOOTER_NAV = """
  <div class="footer-nav">
    <a href="index.html">연봉 실수령액</a>
    <a href="bonus-index.html">성과급 계산기</a>
    <a href="severance.html">퇴직금 계산기</a>
    <a href="about.html">사이트 소개</a>
    <a href="privacy.html">개인정보처리방침</a>
    <a href="contact.html">문의</a>
  </div>
"""

STYLE = """
  body { font-family: -apple-system, "Malgun Gothic", sans-serif; max-width: 640px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; line-height: 1.7; }
  h1 { font-size: 22px; }
  h2 { font-size: 17px; margin-top: 28px; }
  .footer-nav { margin-top: 40px; padding-top: 16px; border-top: 1px solid #eee; font-size: 13px; color: #666; }
  .footer-nav a { color: #666; margin-right: 12px; }
"""


def about_html():
    return f"""<!doctype html>
<html lang="ko">
<head>
{GA_SNIPPET}
<meta charset="utf-8">
<title>사이트 소개 - {SITE_NAME}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{STYLE}</style>
</head>
<body>
  <h1>사이트 소개</h1>
  <p>{SITE_NAME}는 연봉 구간별 4대보험(국민연금·건강보험·장기요양보험·고용보험)과 소득세 공제 내역을
  계산해 예상 월 실수령액을 안내하는 사이트입니다.</p>

  <h2>계산 방식</h2>
  <p>1인 가구, 기본공제만 적용한 단순화된 모델을 기준으로 계산합니다. 부양가족 수, 각종 세액공제,
  비과세 수당 등 개인별 상황에 따라 실제 원천징수 금액과 차이가 있을 수 있습니다. 4대보험 요율은
  매년 변경되므로 사이트 운영자가 주기적으로 최신 고시 수치를 반영하여 갱신합니다.</p>

  <h2>정확한 금액이 필요하다면</h2>
  <p>정확한 원천징수 세액은 국세청 홈택스 또는 재직 중인 회사의 급여 담당 부서를 통해 확인하시기
  바랍니다. 본 사이트의 계산 결과는 참고용 추정치입니다.</p>

{FOOTER_NAV}
</body>
</html>"""


def privacy_html():
    return f"""<!doctype html>
<html lang="ko">
<head>
{GA_SNIPPET}
<meta charset="utf-8">
<title>개인정보처리방침 - {SITE_NAME}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{STYLE}</style>
</head>
<body>
  <h1>개인정보처리방침</h1>
  <p>{SITE_NAME}(이하 '사이트')는 이용자의 개인정보를 소중히 다루며, 다음과 같이 개인정보처리방침을
  안내드립니다.</p>

  <h2>1. 수집하는 개인정보 항목</h2>
  <p>본 사이트는 회원가입이나 로그인 기능이 없으며, 이용자가 직접 입력하는 개인정보를 수집하지
  않습니다. 다만 광고 게재 및 서비스 개선을 위해 Google AdSense, Google Analytics 등 제3자
  서비스를 통해 쿠키 기반의 방문 기록(방문 페이지, 접속 기기, 대략적 위치 등)이 자동 수집될 수
  있습니다.</p>

  <h2>2. 쿠키(Cookie)의 사용</h2>
  <p>본 사이트는 광고 게재를 위해 Google 및 협력사의 쿠키를 사용합니다. 이용자는 브라우저 설정을
  통해 쿠키 저장을 거부할 수 있으며, Google 광고 개인 최적화 설정은
  <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google 광고 설정</a>
  페이지에서 변경할 수 있습니다.</p>

  <h2>3. 제3자 광고 서비스</h2>
  <p>본 사이트는 Google AdSense를 통해 광고를 게재하며, Google은 이용자의 관심사에 기반한 광고를
  제공하기 위해 쿠키를 사용할 수 있습니다. 자세한 내용은 Google의 광고 정책을 참고하시기 바랍니다.</p>

  <h2>4. 문의</h2>
  <p>개인정보처리방침 관련 문의는 <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>로 연락
  주시기 바랍니다.</p>

  <h2>5. 시행일</h2>
  <p>본 방침은 2026년 8월 22일부터 적용됩니다.</p>

{FOOTER_NAV}
</body>
</html>"""


def contact_html():
    return f"""<!doctype html>
<html lang="ko">
<head>
{GA_SNIPPET}
<meta charset="utf-8">
<title>문의 - {SITE_NAME}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{STYLE}</style>
</head>
<body>
  <h1>문의</h1>
  <p>사이트 이용 중 궁금한 점, 오류 제보, 광고/제휴 문의는 아래 이메일로 연락 주시기 바랍니다.</p>
  <p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>

{FOOTER_NAV}
</body>
</html>"""
