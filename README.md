# 연봉 실수령액 계산기 (프로그래매틱 SEO 데모)

## 구조
- `calc.py` — 4대보험/소득세 계산 로직 (요율은 2025년 예시값, 매년 갱신 필요)
- `static_pages.py` — about/privacy/contact 페이지 (SITE_NAME, CONTACT_EMAIL 여기서 수정)
- `generate.py` — 연봉 구간별 페이지 + index.html + sitemap.xml 대량 생성
- `output/` — 생성된 정적 사이트 (이 폴더 전체를 배포하면 됨)

## 로컬에서 다시 생성하기
```bash
python generate.py
```
`generate.py` 상단의 `START`/`END`/`STEP`을 바꾸면 페이지 개수가 조절됩니다
(예: STEP을 100_000으로 줄이면 페이지가 8배로 늘어남).

## 배포 전 반드시 할 일
1. `generate.py`의 `BASE_URL`을 실제 구매한 도메인으로 교체
2. `static_pages.py`의 `CONTACT_EMAIL`을 실제 연락처로 교체
3. `calc.py`의 4대보험 요율/상한액을 최신 공식 고시 수치로 검증
4. 도메인 구매 (가비아, 카페24, Namecheap 등 — 연 1~2만원대)

## 배포 방법 (Vercel, 무료)
Vercel 계정 생성과 로그인은 본인이 직접 해야 합니다 (브라우저 인증 필요).

1. https://vercel.com 가입 (GitHub 계정으로 가입 추천)
2. 터미널에서:
   ```bash
   npm i -g vercel
   cd output
   vercel --prod
   ```
   (Node.js 설치가 안 되어 있으면 https://nodejs.org 에서 먼저 설치)
3. 배포 후 Vercel 대시보드에서 "Domains"에 구매한 도메인 연결

## 검색엔진 등록
1. [Google Search Console](https://search.google.com/search-console) — 도메인 소유권 확인 후 `sitemap.xml` 제출
2. [네이버 서치어드바이저](https://searchadvisor.naver.com) — 동일하게 사이트 등록 + sitemap 제출

## 애드센스 신청 전 체크리스트
- [ ] 실제 도메인 연결 완료
- [ ] 검색엔진에 색인 시작 (제출 후 1~2주 소요)
- [ ] privacy/about/contact 페이지 정상 작동 확인
- [ ] 최소 2~4주 실 방문자 데이터 축적 권장
- [ ] https://www.google.com/adsense 에서 사이트 등록 후 심사 신청
