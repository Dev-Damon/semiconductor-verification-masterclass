/* 공용 슬라이드 엔진 — 의존성 없음(오프라인 동작)
   사용법: 각 챕터 HTML에서 <body data-title="챕터명"> + .slide 섹션들 + 이 스크립트 로드
   마지막 슬라이드에서 '다음 챕터' 버튼/이동 지원 */
(function () {
  // 이 트랙(검증)의 챕터 순서 — 개념판(chapters/)과 심화판(advanced/chapters/) 공통 파일명
  var ORDER = ['ch0-1','ch0-2','ch0-3','ch1-1','ch1-2','ch2-1','ch2-2','ch3-1','ch3-2','ch3-3','ch4-1','ch4-2','ch4-3','ch5-1','ch5-2','ch5-3','ch6-1','ch6-2','ch7-1'];

  function init() {
    var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
    if (!slides.length) return;
    var i = 0;
    var title = document.body.getAttribute('data-title') || '';

    // 다음 챕터 계산 (같은 디렉터리 내에서 이동 → 개념판/심화판 트랙 유지)
    var curFile = (location.pathname.split('/').pop() || '').replace('.html', '');
    var idx = ORDER.indexOf(curFile), nextHref, nextLabel;
    if (idx >= 0 && idx < ORDER.length - 1) {
      var nx = ORDER[idx + 1];
      nextHref = nx + '.html';
      nextLabel = '다음 챕터 ' + nx.replace(/^ch/, '').replace(/^dp/, '') + ' →';
    } else {
      nextHref = '../index.html';
      nextLabel = '전체 목차로 →';
    }
    function gotoNext() { if (nextHref) location.href = nextHref; }

    // chrome 주입
    var bar = document.createElement('div'); bar.className = 'progress'; document.body.appendChild(bar);
    var home = document.createElement('a'); home.className = 'home-link'; home.href = '../index.html'; home.innerHTML = '← 목차'; document.body.appendChild(home);
    var hud = document.createElement('div'); hud.className = 'hud';
    hud.innerHTML =
      '<div class="title">' + title + '</div>' +
      '<div class="nav">' +
        '<button data-prev aria-label="이전">‹</button>' +
        '<span class="counter"><b data-cur>1</b> / ' + slides.length + '</span>' +
        '<button data-next aria-label="다음">›</button>' +
      '</div>';
    document.body.appendChild(hud);
    var cur = hud.querySelector('[data-cur]');

    // 마지막 슬라이드용 '다음 챕터' 버튼
    var cta = document.createElement('a');
    cta.href = nextHref; cta.textContent = nextLabel;
    cta.style.cssText = 'position:fixed;left:50%;bottom:64px;transform:translateX(-50%);z-index:42;display:none;' +
      'background:linear-gradient(90deg,var(--accent),var(--accent2));color:#06121f;font-weight:800;font-size:14px;' +
      'padding:11px 24px;border-radius:30px;text-decoration:none;box-shadow:0 12px 34px rgba(0,0,0,.45);white-space:nowrap';
    document.body.appendChild(cta);

    function show(n) {
      i = Math.max(0, Math.min(slides.length - 1, n));
      slides.forEach(function (s, k) { s.classList.toggle('active', k === i); });
      bar.style.width = ((i) / (slides.length - 1) * 100) + '%';
      if (slides.length === 1) bar.style.width = '100%';
      cur.textContent = i + 1;
      cta.style.display = (i === slides.length - 1) ? 'inline-block' : 'none';
      if (location.hash !== '#' + (i + 1)) history.replaceState(null, '', '#' + (i + 1));
      var a = slides[i]; if (a) a.scrollTop = 0;
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); if (i === slides.length - 1) gotoNext(); else show(i + 1); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); show(i - 1); }
      else if (e.key === 'Home') show(0);
      else if (e.key === 'End') show(slides.length - 1);
    });
    hud.querySelector('[data-next]').addEventListener('click', function () { if (i === slides.length - 1) gotoNext(); else show(i + 1); });
    hud.querySelector('[data-prev]').addEventListener('click', function () { show(i - 1); });

    // 좌/우 화면 클릭으로도 넘김(코드/링크 클릭은 제외)
    document.addEventListener('click', function (e) {
      if (e.target.closest('a,button,pre,table,.no-advance')) return;
      var x = e.clientX / window.innerWidth;
      if (x > 0.82) { if (i === slides.length - 1) gotoNext(); else show(i + 1); }
      else if (x < 0.18) show(i - 1);
    });

    var start = parseInt((location.hash || '').replace('#', ''), 10);
    show(isNaN(start) ? 0 : start - 1);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
