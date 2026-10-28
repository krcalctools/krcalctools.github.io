"""
연봉 티어 테스트 - "내 연봉은 상위 몇 %?" 인터랙티브 페이지 (docs/salary-rank.html)

숫자의 출처는 두 가지이고 섞지 않는다:
- 전체 순위(상위 %, 100명 중 몇 등, 티어): 국세청 연간 총급여 백분위 -> income_percentile.py
- 성별·연령대 안에서의 위치, 업종 비교: 국가데이터처 월 보수 분포 -> kostat_income.py
티어 이름과 업종 티어 컷은 재미용 구분이라 기준을 페이지에 그대로 공개한다.
결과는 URL 파라미터(?s=연봉&g=성별&a=나이대&i=업종)로 재현돼서 링크 공유가 곧 결과 공유다.
"""
import json
import os

import generate
from income_percentile import PERCENTILE_TABLE, TOTAL_WORKERS, DATA_YEAR, SOURCE_NOTE, estimate_top_percent
from kostat_income import (BANDS, DIST, AGE_LABELS, MEAN, MEAN_BY_SEX_AGE, MEDIAN_ALL, INDUSTRIES,
                           INDUSTRY_TIER_CUTS, industry_tier, DATA_LABEL, SOURCE_URL as KOSTAT_URL)
from static_pages import GA_SNIPPET, FOOTER_NAV, SITE_STYLE, SITE_HEADER, FAVICON, seo_meta

OUTPUT_DIR = generate.OUTPUT_DIR
FILENAME = "salary-rank.html"
NTS_URL = "https://www.data.go.kr/data/15082063/fileData.do"

# (상한 상위 %, 키, 이모지, 이름, 한 줄 코멘트) - 위에서부터 처음 맞는 티어
TIERS = [
    (1, "legend", "👑", "레전드", "대한민국 직장인 꼭대기. 연말정산이 무서운 구간"),
    (5, "diamond", "💎", "다이아", "100명이 모이면 맨 앞줄에 앉는 사람"),
    (15, "platinum", "💠", "플래티넘", "어디 가서 연봉 얘기 먼저 꺼내도 되는 구간"),
    (30, "gold", "🥇", "골드", "평균은 가볍게 넘긴 탄탄한 상위권"),
    (50, "silver", "🥈", "실버", "중간보다 위. 여기서부터가 진짜 경쟁"),
    (75, "bronze", "🥉", "브론즈", "직장인 절반 가까이가 여기서 출발해요"),
    (100, "sprout", "🌱", "새싹", "시작이 반! 성장 그래프는 지금부터"),
]

FAQ = [
    ("연봉 상위 10%는 얼마부터인가요?",
     f"국세청 {DATA_YEAR}년 귀속 자료로 추정하면 연봉(총급여) 약 {dict(PERCENTILE_TABLE)[10]:,}만원부터 상위 10%입니다."),
    ("우리나라 직장인 중위 연봉은 얼마인가요?",
     f"근로소득자를 연봉 순으로 줄 세웠을 때 한가운데(상위 50%)는 약 {dict(PERCENTILE_TABLE)[50]:,}만원입니다. "
     f"평균은 고소득자에게 끌려 올라가서 중위값보다 높습니다."),
    ("사이트마다 '상위 몇 %' 결과가 다른 이유는요?",
     "국세청은 구간별 합계만 공개하고 커트라인은 공개하지 않아서, 경계를 추정하는 방법에 따라 결과가 달라집니다. "
     "이 페이지는 이웃한 두 구간 평균의 기하평균을 경계로 씁니다. 또 '근로자 전체'인지 '1년 내내 일한 사람만'인지에 따라서도 달라집니다."),
    ("성별·나이대 비교는 왜 월급 기준인가요?",
     "성별·나이대별 소득 분포는 국가데이터처 '임금근로일자리 소득' 통계에만 있고, 이 통계가 월 평균 보수 기준이기 때문입니다. "
     "그래서 입력한 연봉을 12로 나눈 월급으로 비교합니다. 시간제 일자리까지 포함한 통계라 전체 순위보다 조금 후하게 나올 수 있습니다."),
    ("입력한 연봉이 어디로 전송되나요?",
     "아니요. 모든 계산은 브라우저 안에서만 이뤄지고, 공유 버튼을 누를 때만 결과가 링크 주소에 담깁니다."),
]


def cutline_rows():
    table = dict(PERCENTILE_TABLE)
    return "\n".join(
        f'<tr><td>상위 {p}%</td><td class="num">{table[p]:,}만원</td><td class="num">{table[p] / 12:,.0f}만원</td></tr>'
        for p in (1, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90)
    )


def sex_age_rows():
    return "\n".join(
        f'<tr><td>{label}</td><td class="num">{MEAN_BY_SEX_AGE["male"][k]:,}만원</td>'
        f'<td class="num">{MEAN_BY_SEX_AGE["female"][k]:,}만원</td><td class="num">{MEAN[k]:,}만원</td></tr>'
        for k, label in AGE_LABELS.items()
    )


def tier_rule_rows():
    prev = 0
    rows = []
    for cap, key, emoji, name, _ in TIERS:
        rng = f"상위 {cap}% 이내" if prev == 0 else f"상위 {prev}~{cap}%"
        lo = dict(PERCENTILE_TABLE).get(cap)
        cut = f"약 {lo:,}만원 이상" if cap < 100 and lo else "-"
        rows.append(f'<tr><td>{emoji} {name}</td><td>{rng}</td><td class="num">{cut}</td></tr>')
        prev = cap
    return "\n".join(rows)


def industry_tier_html():
    groups = []
    for tier, _ in INDUSTRY_TIER_CUTS:
        items = "".join(
            f'<span class="ind-chip" data-ind="{code}">{name}<small>{mean}만</small></span>'
            for code, name, mean, _ in INDUSTRIES if industry_tier(mean) == tier
        )
        if items:
            groups.append(f'<div class="tier-row"><div class="tier-label t-{tier}">{tier}</div><div class="tier-items">{items}</div></div>')
    return "\n".join(groups)


PAGE_STYLE = """
  :root {
    --rank-grad-a: #1d2b53; --rank-grad-b: #3b1d5a; --rank-grad-c: #0f3d3e;
    --chip-bg: #1b212c; --chip-on: #60a5fa; --chip-on-text: #0b1220;
    --dot-off: #2a313d; --dot-on: #fbbf24; --dot-me: #f472b6;
    --t-legend: #fbbf24; --t-diamond: #67e8f9; --t-platinum: #5eead4; --t-gold: #facc15;
    --t-silver: #cbd5e1; --t-bronze: #d97706; --t-sprout: #4ade80;
    --tier-s: #f472b6; --tier-a: #fb923c; --tier-b: #facc15; --tier-c: #4ade80; --tier-d: #60a5fa;
    --bar: #334155; --bar-me: #f472b6; --up: #4ade80; --down: #f87171;
  }
  .rank-hero {
    border-radius: 20px; padding: 26px 22px; margin: 10px 0 18px; text-align: center;
    background: linear-gradient(135deg, var(--rank-grad-a), var(--rank-grad-b) 55%, var(--rank-grad-c));
  }
  .rank-hero h1 { margin: 0 0 6px; font-size: 25px; line-height: 1.35; }
  .rank-hero p { margin: 0; color: var(--body-dim); font-size: 14px; }
  .step-label { font-size: 13px; color: var(--muted); font-weight: 600; margin: 16px 0 8px; }
  .chips { display: flex; flex-wrap: wrap; gap: 8px; }
  .chip {
    border: 1px solid var(--border); background: var(--chip-bg); color: var(--text); border-radius: 999px;
    padding: 9px 15px; font-size: 14px; cursor: pointer; transition: transform .12s, background .12s;
  }
  .chip:hover { transform: translateY(-1px); border-color: var(--primary); }
  .chip.on { background: var(--chip-on); color: var(--chip-on-text); border-color: var(--chip-on); font-weight: 700; }
  .salary-input { display: flex; align-items: center; gap: 8px; }
  .salary-input input {
    flex: 1; font-size: 26px; font-weight: 800; padding: 12px 14px; border-radius: 14px;
    border: 1px solid var(--border); background: var(--input-bg); color: var(--text); min-width: 0;
  }
  .salary-input span { font-size: 18px; color: var(--muted); font-weight: 700; }
  .salary-hint { font-size: 12px; color: var(--muted); margin-top: 6px; min-height: 18px; }
  .go-btn {
    width: 100%; margin-top: 20px; padding: 16px; border: 0; border-radius: 14px; cursor: pointer;
    font-size: 17px; font-weight: 800; color: var(--chip-on-text);
    background: linear-gradient(90deg, var(--t-gold), var(--dot-me));
  }
  .go-btn:active { transform: scale(.98); }
  #result { display: none; }
  .reveal { animation: pop .5s ease-out; }
  @keyframes pop { from { opacity: 0; transform: translateY(14px) scale(.97); } to { opacity: 1; transform: none; } }
  .result-card {
    border-radius: 22px; padding: 26px 20px; text-align: center; margin: 18px 0;
    background: radial-gradient(circle at 50% 0%, var(--rank-grad-b), var(--card-bg) 70%);
    border: 1px solid var(--border);
  }
  .tier-emoji { font-size: 64px; line-height: 1; filter: drop-shadow(0 0 18px var(--tier-glow, transparent)); }
  .tier-name { font-size: 22px; font-weight: 900; margin-top: 6px; color: var(--tier-color, var(--text)); }
  .big-pct { font-size: 52px; font-weight: 900; letter-spacing: -1px; margin: 4px 0; }
  .big-pct small { font-size: 22px; font-weight: 700; color: var(--muted); }
  .tier-caption { color: var(--body-dim); font-size: 14px; }
  .rank-line { margin-top: 12px; font-size: 15px; }
  .rank-line b { color: var(--dot-on); }
  .dots { display: grid; grid-template-columns: repeat(20, 1fr); gap: 4px; max-width: 360px; margin: 16px auto 4px; }
  .dots i { aspect-ratio: 1; border-radius: 50%; background: var(--dot-off); transition: background .25s; }
  .dots i.above { background: var(--dot-on); }
  .dots i.me { background: var(--dot-me); box-shadow: 0 0 0 3px rgba(244,114,182,.35); }
  .dots-legend { font-size: 12px; color: var(--muted); }
  .cmp-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0; }
  .cmp {
    background: var(--card-bg); border: 1px solid var(--border); border-radius: 14px; padding: 14px; text-align: left;
  }
  .cmp .k { font-size: 12px; color: var(--muted); }
  .cmp .v { font-size: 22px; font-weight: 800; margin-top: 2px; }
  .cmp .s { font-size: 12px; color: var(--body-dim); margin-top: 2px; }
  .up { color: var(--up); } .down { color: var(--down); }
  @media (max-width: 420px) { .cmp-grid { grid-template-columns: 1fr; } .big-pct { font-size: 44px; } }
  .histo { width: 100%; height: auto; margin-top: 6px; }
  .histo rect.b { fill: var(--bar); } .histo rect.me { fill: var(--bar-me); }
  .histo text { fill: var(--muted); font-size: 10px; }
  .histo .me-label { fill: var(--bar-me); font-size: 11px; font-weight: 700; }
  .share-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
  .share-row button {
    flex: 1; min-width: 120px; padding: 12px; border-radius: 12px; border: 1px solid var(--border);
    background: var(--chip-bg); color: var(--text); font-size: 14px; font-weight: 700; cursor: pointer;
  }
  .share-row button.primary { background: var(--chip-on); color: var(--chip-on-text); border-color: var(--chip-on); }
  .toast { font-size: 13px; color: var(--good-text); min-height: 20px; margin-top: 6px; text-align: center; }
  .tier-row { display: flex; gap: 10px; align-items: stretch; margin: 8px 0; }
  .tier-label {
    width: 44px; flex-shrink: 0; border-radius: 10px; display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 20px; color: var(--chip-on-text);
  }
  .t-S { background: var(--tier-s); } .t-A { background: var(--tier-a); } .t-B { background: var(--tier-b); }
  .t-C { background: var(--tier-c); } .t-D { background: var(--tier-d); }
  .tier-items { display: flex; flex-wrap: wrap; gap: 6px; flex: 1; }
  .ind-chip {
    background: var(--chip-bg); border: 1px solid var(--border); border-radius: 10px; padding: 6px 10px; font-size: 13px;
  }
  .ind-chip small { margin-left: 6px; color: var(--muted); }
  .ind-chip.mine { border-color: var(--dot-me); box-shadow: 0 0 0 2px rgba(244,114,182,.35); }
  .faq details { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px; margin: 8px 0; }
  .faq summary { cursor: pointer; font-weight: 700; font-size: 14px; }
  .faq p { margin: 8px 0 0; font-size: 14px; color: var(--body-dim); }
"""

# JS는 f-string 밖에 둬서 중괄호 이스케이프 없이 쓴다. 데이터만 DATA_JS로 주입.
APP_JS = r"""
const $ = (id) => document.getElementById(id);
const state = { s: null, g: null, a: null, i: '' };
const AGE_KEYS = Object.keys(D.ageLabels);

function topPercent(man) {
  const t = D.nts;
  if (man >= t[0][1]) return t[0][0];
  if (man <= t[t.length - 1][1]) return t[t.length - 1][0];
  for (let k = 0; k < t.length - 1; k++) {
    const [pHi, vHi] = t[k], [pLo, vLo] = t[k + 1];
    if (vLo <= man && man <= vHi) return Math.round((pLo - (man - vLo) / (vHi - vLo) * (pLo - pHi)) * 10) / 10;
  }
  return t[t.length - 1][0];
}
function topInGroup(monthly, key) {
  const dist = D.dist[key], b = D.bands;
  if (monthly >= b[b.length - 1]) return { pct: dist[dist.length - 1], capped: true };
  let below = 0;
  for (let k = 0; k < dist.length - 1; k++) {
    if (monthly < b[k + 1]) { below += dist[k] * (monthly - b[k]) / (b[k + 1] - b[k]); break; }
    below += dist[k];
  }
  return { pct: Math.round((100 - below) * 10) / 10, capped: false };
}
function tierOf(p) { return D.tiers.find(t => p <= t[0]); }
function fmtMan(m) {
  m = Math.round(m);
  if (m >= 10000) { const e = Math.floor(m / 10000), r = m % 10000; return e + '억' + (r ? ' ' + r.toLocaleString() + '만' : '') + '원'; }
  return m.toLocaleString() + '만원';
}
function pctText(p) { return p < 0.1 ? '0.1' : (p >= 10 ? Math.round(p) : p.toFixed(1)); }

function pick(group, val, el) {
  state[group] = (state[group] === val) ? null : val;
  document.querySelectorAll('[data-group="' + group + '"]').forEach(c => c.classList.toggle('on', c.dataset.val === state[group]));
}
function setSalary(v) { $('salary').value = Number(v).toLocaleString(); onSalary(); }
function onSalary() {
  const raw = $('salary').value.replace(/[^0-9]/g, '');
  let v = Number(raw);
  // 원 단위로 입력한 경우(예: 45000000) 만원으로 보정
  if (v > 1000000) v = Math.round(v / 10000);
  state.s = v || null;
  $('salary-hint').textContent = v ? '= ' + fmtMan(v) + ' · 월 약 ' + Math.round(v / 12).toLocaleString() + '만원' : '';
}

function animateNumber(el, to, ms) {
  const start = performance.now(), from = 100;
  function step(now) {
    const k = Math.min(1, (now - start) / ms), e = 1 - Math.pow(1 - k, 3);
    el.textContent = pctText(from + (to - from) * e);
    if (k < 1) requestAnimationFrame(step); else el.textContent = pctText(to);
  }
  requestAnimationFrame(step);
}

function histogram(monthly) {
  const dist = D.dist.all, b = D.bands, W = 340, H = 150, n = dist.length, bw = W / n, max = Math.max(...dist);
  let meIdx = b.findIndex((x, k) => monthly >= x && (k === n - 1 || monthly < b[k + 1]));
  let svg = '<svg class="histo" viewBox="0 0 ' + W + ' ' + (H + 34) + '" role="img" aria-label="월 소득 구간별 근로자 분포">';
  dist.forEach((v, k) => {
    const h = v / max * (H - 18), x = k * bw + 3, y = H - h;
    svg += '<rect class="' + (k === meIdx ? 'me' : 'b') + '" x="' + x + '" y="' + y + '" width="' + (bw - 6) + '" height="' + h + '" rx="4"></rect>';
    svg += '<text x="' + (x + (bw - 6) / 2) + '" y="' + (y - 4) + '" text-anchor="middle">' + v + '%</text>';
    const lab = k === n - 1 ? '1000+' : b[k] + '~';
    svg += '<text x="' + (x + (bw - 6) / 2) + '" y="' + (H + 14) + '" text-anchor="middle">' + lab + '</text>';
    if (k === meIdx) svg += '<text class="me-label" x="' + (x + (bw - 6) / 2) + '" y="' + (H + 30) + '" text-anchor="middle">▲ 나</text>';
  });
  return svg + '</svg>';
}

function cmpCard(k, v, s, cls) {
  return '<div class="cmp"><div class="k">' + k + '</div><div class="v ' + (cls || '') + '">' + v + '</div><div class="s">' + s + '</div></div>';
}

function run(scroll) {
  onSalary();
  if (!state.s) { $('salary').focus(); $('salary-hint').textContent = '연봉을 먼저 입력해 주세요 🙏'; return; }
  const s = state.s, monthly = s / 12, p = topPercent(s), t = tierOf(p);
  const res = $('result');
  res.style.display = 'block'; res.classList.remove('reveal'); void res.offsetWidth; res.classList.add('reveal');

  const card = $('card');
  card.style.setProperty('--tier-color', 'var(--t-' + t[1] + ')');
  card.style.setProperty('--tier-glow', 'var(--t-' + t[1] + ')');
  $('tier-emoji').textContent = t[2];
  $('tier-name').textContent = t[3] + ' 티어';
  $('tier-caption').textContent = t[4];
  animateNumber($('pct'), p, 900);

  const rank = Math.max(1, Math.ceil(p));
  $('rank-line').innerHTML = '대한민국 직장인 100명 중 <b>' + rank + '등</b> · 전체 ' + D.totalMan.toLocaleString() + '만 명 중 약 <b>' + Math.max(1, Math.round(D.totalMan * p / 100)).toLocaleString() + '만 등</b>';
  const dots = $('dots'); dots.innerHTML = '';
  for (let k = 1; k <= 100; k++) {
    const d = document.createElement('i');
    if (k < rank) d.className = 'above'; else if (k === rank) d.className = 'me';
    dots.appendChild(d);
  }

  let cards = '';
  if (state.g) {
    const r = topInGroup(monthly, state.g), label = state.g === 'male' ? '남성' : '여성';
    cards += cmpCard(label + ' 직장인 중', (r.capped ? '상위 ' + r.pct + '% 이내' : '상위 ' + pctText(r.pct) + '%'), '월 ' + Math.round(monthly).toLocaleString() + '만원 기준 · 평균 ' + D.mean[state.g] + '만원');
  }
  if (state.a) {
    const r = topInGroup(monthly, state.a);
    cards += cmpCard(D.ageLabels[state.a] + ' 직장인 중', (r.capped ? '상위 ' + r.pct + '% 이내' : '상위 ' + pctText(r.pct) + '%'), D.ageLabels[state.a] + ' 평균 월 ' + D.mean[state.a] + '만원');
  }
  if (state.g && state.a) {
    const avg = D.sexAge[state.g][state.a], diff = Math.round(monthly - avg);
    cards += cmpCard('같은 ' + D.ageLabels[state.a] + ' ' + (state.g === 'male' ? '남성' : '여성') + ' 평균보다', (diff >= 0 ? '+' : '') + diff.toLocaleString() + '만원', '평균 월 ' + avg + '만원 vs 나 월 ' + Math.round(monthly).toLocaleString() + '만원', diff >= 0 ? 'up' : 'down');
  }
  if (state.i) {
    const ind = D.industries.find(x => x[0] === state.i), diff = Math.round(monthly - ind[2]);
    cards += cmpCard(ind[1] + ' (' + ind[4] + '티어 업종)', (diff >= 0 ? '+' : '') + diff.toLocaleString() + '만원', '업종 평균 월 ' + ind[2] + '만원 · 중위 ' + ind[3] + '만원', diff >= 0 ? 'up' : 'down');
  }
  if (!cards) cards = cmpCard('더 재밌게 보려면', '성별·나이대 선택', '위에서 고르면 같은 또래·같은 성별 안에서의 순위도 나와요');
  $('cmp').innerHTML = cards;
  $('histo').innerHTML = histogram(monthly);
  document.querySelectorAll('.ind-chip').forEach(c => c.classList.toggle('mine', c.dataset.ind === state.i));

  const q = new URLSearchParams({ s: s });
  if (state.g) q.set('g', state.g); if (state.a) q.set('a', state.a); if (state.i) q.set('i', state.i);
  history.replaceState(null, '', '?' + q.toString());
  if (window.gtag) gtag('event', 'rank_calc', { tier: t[1], top_pct: Math.round(p) });
  if (scroll) res.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function shareUrl() { return location.href.split('#')[0]; }
function shareText() {
  const p = topPercent(state.s), t = tierOf(p);
  return '내 연봉은 대한민국 직장인 상위 ' + pctText(p) + '% ' + t[2] + t[3] + ' 티어! 너는 몇 티어야?';
}
function toast(msg) { $('toast').textContent = msg; setTimeout(() => $('toast').textContent = '', 2500); }
async function copyLink() {
  try { await navigator.clipboard.writeText(shareText() + ' ' + shareUrl()); toast('링크를 복사했어요. 친구한테 붙여넣기!'); }
  catch (e) { prompt('아래 링크를 복사하세요', shareUrl()); }
}
async function nativeShare() {
  if (navigator.share) { try { await navigator.share({ title: '연봉 티어 테스트', text: shareText(), url: shareUrl() }); } catch (e) {} }
  else copyLink();
}
function saveImage() {
  const p = topPercent(state.s), t = tierOf(p), c = document.createElement('canvas'), W = 1080, H = 1350;
  c.width = W; c.height = H;
  const x = c.getContext('2d'), css = getComputedStyle(document.documentElement);
  const v = (n) => css.getPropertyValue(n).trim();
  const g = x.createLinearGradient(0, 0, W, H);
  g.addColorStop(0, v('--rank-grad-a')); g.addColorStop(.55, v('--rank-grad-b')); g.addColorStop(1, v('--rank-grad-c'));
  x.fillStyle = g; x.fillRect(0, 0, W, H);
  x.textAlign = 'center'; x.fillStyle = v('--text');
  x.font = '700 44px sans-serif'; x.fillText('내 연봉 티어는?', W / 2, 170);
  x.font = '220px sans-serif'; x.fillText(t[2], W / 2, 470);
  x.fillStyle = v('--t-' + t[1]); x.font = '900 96px sans-serif'; x.fillText(t[3], W / 2, 620);
  x.fillStyle = v('--text'); x.font = '900 150px sans-serif'; x.fillText('상위 ' + pctText(p) + '%', W / 2, 820);
  x.font = '600 46px sans-serif'; x.fillStyle = v('--body-dim');
  x.fillText('직장인 100명 중 ' + Math.max(1, Math.ceil(p)) + '등', W / 2, 920);
  x.font = '500 34px sans-serif'; x.fillText(t[4], W / 2, 1000);
  x.font = '600 32px sans-serif'; x.fillStyle = v('--muted');
  x.fillText('국세청 ' + D.year + '년 귀속 근로소득 기준', W / 2, 1180);
  x.fillText('krcalctools.github.io/salary-rank', W / 2, 1230);
  c.toBlob(async (blob) => {
    const file = new File([blob], '내-연봉-티어.png', { type: 'image/png' });
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      try { await navigator.share({ files: [file], text: shareText() }); return; } catch (e) {}
    }
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = file.name; a.click();
    toast('이미지를 저장했어요 📸');
  });
}

document.querySelectorAll('.chip[data-group]').forEach(c => c.addEventListener('click', () => pick(c.dataset.group, c.dataset.val)));
$('salary').addEventListener('input', onSalary);
$('salary').addEventListener('keydown', e => { if (e.key === 'Enter') run(true); });
$('industry').addEventListener('change', e => { state.i = e.target.value; });
(function restore() {
  const q = new URLSearchParams(location.search);
  if (q.get('g')) pick('g', q.get('g'));
  if (q.get('a') && AGE_KEYS.includes(q.get('a'))) pick('a', q.get('a'));
  if (q.get('i')) { $('industry').value = q.get('i'); state.i = q.get('i'); }
  if (q.get('s')) { setSalary(q.get('s')); run(false); }
})();
"""


def data_js():
    data = {
        "nts": PERCENTILE_TABLE,
        "year": DATA_YEAR,
        "totalMan": round(TOTAL_WORKERS / 10000),
        "bands": BANDS,
        "dist": DIST,
        "mean": MEAN,
        "sexAge": MEAN_BY_SEX_AGE,
        "ageLabels": AGE_LABELS,
        "industries": [[c, n, m, med, industry_tier(m)] for c, n, m, med in INDUSTRIES],
        "tiers": [list(t) for t in TIERS],
    }
    return "const D = " + json.dumps(data, ensure_ascii=False) + ";"


def rank_html():
    title = f"연봉 상위 몇 %? 내 연봉 티어 테스트 ({DATA_YEAR}년 국세청 자료)"
    desc = (f"연봉을 입력하면 대한민국 직장인 중 상위 몇 %인지, 100명 중 몇 등인지 바로 알려드려요. "
            f"성별·나이대 안에서의 순위와 업종 티어까지. 국세청 근로자 {TOTAL_WORKERS / 10000:,.0f}만 명 원자료 기준.")
    age_chips = "".join(f'<button type="button" class="chip" data-group="a" data-val="{k}">{v}</button>' for k, v in AGE_LABELS.items())
    ind_options = "".join(f'<option value="{c}">{n}</option>' for c, n, _, _ in INDUSTRIES)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    faq_html = "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    examples = " · ".join(
        f'연봉 {s:,}만원 = 상위 {estimate_top_percent(s)}%' for s in (3000, 4000, 5000, 7000, 10000))

    return f"""<!doctype html>
<html lang="ko">
<head>
{GA_SNIPPET}
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{desc}">
{seo_meta(FILENAME, title, desc, app_name="연봉 티어 테스트")}
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
{FAVICON}
<style>{SITE_STYLE}{PAGE_STYLE}</style>
</head>
<body>
{SITE_HEADER}
  <div class="rank-hero">
    <h1>내 연봉, 대한민국 상위 몇 %? 🏆</h1>
    <p>연봉만 넣으면 끝. 직장인 {TOTAL_WORKERS / 10000:,.0f}만 명 중 내 자리를 찾아드려요</p>
  </div>

  <div class="calc-box">
    <div class="step-label">① 세전 연봉 (만원)</div>
    <div class="salary-input">
      <input id="salary" inputmode="numeric" autocomplete="off" placeholder="예: 4,500" aria-label="세전 연봉(만원)">
      <span>만원</span>
    </div>
    <div class="salary-hint" id="salary-hint"></div>
    <div class="chips" style="margin-top:6px">
      <button type="button" class="chip" onclick="setSalary(3000)">3천</button>
      <button type="button" class="chip" onclick="setSalary(4000)">4천</button>
      <button type="button" class="chip" onclick="setSalary(5000)">5천</button>
      <button type="button" class="chip" onclick="setSalary(7000)">7천</button>
      <button type="button" class="chip" onclick="setSalary(10000)">1억</button>
    </div>

    <div class="step-label">② 성별 <span class="source">(선택)</span></div>
    <div class="chips">
      <button type="button" class="chip" data-group="g" data-val="male">🙋‍♂️ 남성</button>
      <button type="button" class="chip" data-group="g" data-val="female">🙋‍♀️ 여성</button>
    </div>

    <div class="step-label">③ 나이대 <span class="source">(선택)</span></div>
    <div class="chips">{age_chips}</div>

    <div class="step-label">④ 업종 <span class="source">(선택)</span></div>
    <div class="field" style="margin:0">
      <select id="industry"><option value="">선택 안 함</option>{ind_options}</select>
    </div>

    <button type="button" class="go-btn" onclick="run(true)">내 티어 확인하기 →</button>
  </div>

  <div id="result">
    <div class="result-card" id="card">
      <div class="tier-emoji" id="tier-emoji"></div>
      <div class="tier-name" id="tier-name"></div>
      <div class="big-pct"><small>상위</small> <span id="pct">100</span><small>%</small></div>
      <div class="tier-caption" id="tier-caption"></div>
      <div class="rank-line" id="rank-line"></div>
      <div class="dots" id="dots" aria-hidden="true"></div>
      <div class="dots-legend">🟡 나보다 연봉이 높은 사람 · 🩷 나</div>
    </div>

    <div class="cmp-grid" id="cmp"></div>

    <h2>월급 구간별 직장인 분포</h2>
    <div id="histo"></div>
    <p class="source">세로 막대 = 각 월 소득 구간(만원)에 속한 근로자 비중. 국가데이터처 {DATA_LABEL}.</p>

    <div class="share-row">
      <button type="button" class="primary" onclick="saveImage()">📸 결과 이미지 저장</button>
      <button type="button" onclick="nativeShare()">📤 공유하기</button>
      <button type="button" onclick="copyLink()">🔗 링크 복사</button>
    </div>
    <div class="toast" id="toast"></div>

    <div class="cross-link-box">
      💸 이 연봉의 실제 월급은? <a href="index.html">연봉 실수령액 계산기</a>로 세금·4대보험 뺀 금액을 확인해 보세요.
    </div>
  </div>

  <h2>업종 티어표 🏢</h2>
  <p class="source">업종별 평균 월급(국가데이터처 {DATA_LABEL}) 기준. S 650만↑ · A 480만↑ · B 400만↑ · C 300만↑ · D 그 아래. 업종을 고르면 내 업종이 표시돼요.</p>
  {industry_tier_html()}

  <div class="explain">
    <h2>연봉 상위 % 커트라인 ({DATA_YEAR}년 귀속)</h2>
    <p>국세청 근로소득 백분위 원자료로 추정한 구간 경계입니다. 예: {examples}.</p>
    <div class="table-wrap"><table>
      <tr><th>구간</th><th>연봉(총급여)</th><th>월 환산</th></tr>
      {cutline_rows()}
    </table></div>

    <h2>티어 기준</h2>
    <table>
      <tr><th>티어</th><th>범위</th><th>연봉</th></tr>
      {tier_rule_rows()}
    </table>

    <h2>성별·나이대별 평균 월급</h2>
    <div class="table-wrap"><table>
      <tr><th>나이대</th><th>남성</th><th>여성</th><th>전체</th></tr>
      {sex_age_rows()}
    </table></div>
    <p>전체 평균 월급은 {MEAN['all']}만원, 중위값은 {MEDIAN_ALL}만원입니다. 평균은 고소득자 쪽으로 끌려가서 중위값보다 높아요.</p>

    <h2>어떻게 계산하나요?</h2>
    <ol class="steps">
      <li><b>전체 순위·티어</b>: 국세청이 공개한 {DATA_YEAR}년 귀속 근로소득 백분위(천분위) 자료의 구간별 인원·총급여 합계로 각 구간 평균을 구하고, 이웃 구간 평균의 기하평균을 경계로 잡아 보간합니다.</li>
      <li><b>성별·나이대 순위</b>: 국가데이터처 「임금근로일자리 소득(보수)」의 월 소득 구간 분포를 쓰고, 구간 안에서는 고르게 분포한다고 보고 보간합니다. 입력한 연봉 ÷ 12로 비교합니다.</li>
      <li><b>같은 성별·나이대 평균</b>: 이 조합은 분포가 공개되지 않아 순위 대신 평균과의 차이만 보여줍니다.</li>
    </ol>
  </div>

  <div class="faq">
    <h2>자주 묻는 질문</h2>
    {faq_html}
  </div>

  <div class="disclaimer">
    출처: <a href="{NTS_URL}" target="_blank" rel="noopener">국세청 근로소득 백분위(천분위) 자료</a>({SOURCE_NOTE}),
    <a href="{KOSTAT_URL}" target="_blank" rel="noopener">국가데이터처 2024년 임금근로일자리 소득(보수) 결과</a>.
    티어 이름과 업종 티어는 재미를 위한 구분입니다. 결과는 통계 기반 추정치이며 입력값은 서버로 전송되지 않습니다.
  </div>
{FOOTER_NAV}
<script>{data_js()}{APP_JS}</script>
</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, FILENAME), "w", encoding="utf-8") as f:
        f.write(rank_html())
    print(f"연봉 티어 테스트 페이지 생성 완료 -> docs/{FILENAME}")


if __name__ == "__main__":
    main()
