/* 공용 슬라이드 엔진 — 의존성 없음(오프라인 동작)
   사용법: 각 챕터 HTML에서 <body data-title="챕터명"> + .slide 섹션들 + 이 스크립트 로드 */
(function () {
  function init() {
    var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
    if (!slides.length) return;
    var i = 0;
    var title = document.body.getAttribute('data-title') || '';

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

    function show(n) {
      i = Math.max(0, Math.min(slides.length - 1, n));
      slides.forEach(function (s, k) { s.classList.toggle('active', k === i); });
      bar.style.width = ((i) / (slides.length - 1) * 100) + '%';
      if (slides.length === 1) bar.style.width = '100%';
      cur.textContent = i + 1;
      if (location.hash !== '#' + (i + 1)) history.replaceState(null, '', '#' + (i + 1));
      var a = slides[i]; if (a) a.scrollTop = 0;
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); show(i + 1); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); show(i - 1); }
      else if (e.key === 'Home') show(0);
      else if (e.key === 'End') show(slides.length - 1);
    });
    hud.querySelector('[data-next]').addEventListener('click', function () { show(i + 1); });
    hud.querySelector('[data-prev]').addEventListener('click', function () { show(i - 1); });

    // 좌/우 화면 클릭으로도 넘김(코드/링크 클릭은 제외)
    document.addEventListener('click', function (e) {
      if (e.target.closest('a,button,pre,table,.no-advance')) return;
      var x = e.clientX / window.innerWidth;
      if (x > 0.82) show(i + 1); else if (x < 0.18) show(i - 1);
    });

    var start = parseInt((location.hash || '').replace('#', ''), 10);
    show(isNaN(start) ? 0 : start - 1);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
