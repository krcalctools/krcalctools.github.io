# 연봉 실수령액 계산기 (프로그래매틱 SEO 데모)

## 구조
- `calc.py` — 4대보험/소득세 계산 로직 (요율은 2025년 예시값, 매년 갱신 필요)
- `static_pages.py` — about/privacy/contact 페이지 (SITE_NAME, CONTACT_EMAIL 여기서 수정)
- `generate.py` — 연봉 구간별 실수령액 페이지 + index.html 생성
- `bonus_data.py` — 삼성전자/SK하이닉스 성과급 지급률 데이터 (뉴스 기반, 반기/연 단위로 갱신 필요)
- `generate_bonus.py` — 성과급(OPI·TAI, PS·PI) 인터랙티브 계산기 페이지 생성
- `build.py` — 위 두 generate 스크립트 + sitemap.xml을 한 번에 빌드 (실제로는 이걸 실행)
- `docs/` — 생성된 정적 사이트 (GitHub Pages가 이 폴더를 그대로 서빙함)

## 로컬에서 다시 생성하기
```bash
python build.py
```
`generate.py` 상단의 `START`/`END`/`STEP`을 바꾸면 연봉 페이지 개수가 조절됩니다
(예: STEP을 100_000으로 줄이면 페이지가 8배로 늘어남).

## 성과급 계산기 지급률 갱신
`bonus_data.py`의 지급률(OPI/TAI, PS/PI)은 삼성전자·SK하이닉스가 반기/연 단위로 새로 발표할 때마다
최신 뉴스를 검색해서 수치와 출처 링크를 갱신해야 합니다. 특히:
- 삼성 TAI 하반기: 매년 12월 말 발표
- 삼성 OPI, SK하이닉스 PS: 매년 1~2월 발표
- SK하이닉스 PI: 반기(7월/1월경)마다 발표

## 배포 전 반드시 할 일
1. `generate.py`의 `BASE_URL`을 실제 구매한 도메인으로 교체
2. `static_pages.py`의 `CONTACT_EMAIL`을 실제 연락처로 교체
3. `calc.py`의 4대보험 요율/상한액을 최신 공식 고시 수치로 검증
4. 도메인 구매 (가비아, 카페24, Namecheap 등 — 연 1~2만원대)

## 배포 방법 (GitHub Pages, 무료 · Node.js 불필요)
GitHub 계정 생성/로그인, 저장소 생성은 본인이 직접 해야 합니다 (브라우저 인증 필요).

1. https://github.com/new 에서 새 저장소 생성 (Public, README 추가 안 함)
2. 로컬에서 저장소 연결 후 push:
   ```bash
   git remote add origin https://github.com/<내계정>/<저장소명>.git
   git branch -M main
   git push -u origin main
   ```
3. 저장소 → Settings → Pages → **Source: Deploy from a branch**,
   **Branch: main / docs** 선택 → Save
4. 1~2분 후 `https://<내계정>.github.io/<저장소명>/` 로 접속 가능

### 계정명 안 보이게 하려면 (커스텀 도메인 연결)
1. 도메인 구매 (가비아/카페24/Namecheap 등)
2. 저장소 → Settings → Pages → **Custom domain**에 구매한 도메인 입력
   → `docs/CNAME` 파일이 자동 생성됨
3. 도메인 등록업체 DNS 설정에서 A레코드를 GitHub Pages IP로 연결
   (185.199.108.153 / .109.153 / .110.153 / .111.153) 또는 www는 CNAME으로
   `<내계정>.github.io` 연결
4. DNS 전파(최대 몇 시간) 후 Pages 설정에서 **Enforce HTTPS** 체크

### 참고: Vercel을 쓰고 싶다면
동일하게 무료지만 Node.js 설치가 필요합니다 (`npm i -g vercel` → `cd docs && vercel --prod`).

## 검색엔진 등록
1. [Google Search Console](https://search.google.com/search-console) — 도메인 소유권 확인 후 `sitemap.xml` 제출
2. [네이버 서치어드바이저](https://searchadvisor.naver.com) — 동일하게 사이트 등록 + sitemap 제출

## 애드센스 신청 전 체크리스트
- [ ] 실제 도메인 연결 완료
- [ ] 검색엔진에 색인 시작 (제출 후 1~2주 소요)
- [ ] privacy/about/contact 페이지 정상 작동 확인
- [ ] 최소 2~4주 실 방문자 데이터 축적 권장
- [ ] https://www.google.com/adsense 에서 사이트 등록 후 심사 신청
