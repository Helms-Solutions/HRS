/* ===== Year in footer ===== */
(function () {
  const y = document.getElementById('yr');
  if (y) y.textContent = new Date().getFullYear();
})();

/* ===== Calendly helpers ===== */
(function () {
  // Handle any element with data-calendly -> open popup widget
  document.addEventListener('click', (e) => {
    const a = e.target.closest('[data-calendly]');
    if (!a) return;
    e.preventDefault();
    if (window.Calendly) {
      Calendly.initPopupWidget({ url: 'https://calendly.com/helmsretirement/15min' });
    } else {
      window.location.href = 'https://calendly.com/helmsretirement/15min';
    }
  });

  // Lead form -> show thank-you card + inline Calendly
  document.querySelectorAll('form.js-lead').forEach((form) => {
    form.addEventListener('submit', (ev) => {
      ev.preventDefault();
      const card = form.closest('.card');
      const ty = card?.parentElement?.querySelector('#thankyou');
      if (card && ty) {
        card.hidden = true;
        ty.hidden = false;

        // Inline Calendly
        const el = ty.querySelector('#calendly-inline-widget');
        if (el && window.Calendly) {
          Calendly.initInlineWidget({
            url: 'https://calendly.com/helmsretirement/15min',
            parentElement: el,
            prefill: {},
            utm: {}
          });
        } else if (el) {
          // Fallback: simple iframe if Calendly library hasn’t loaded yet
          el.innerHTML =
            '<iframe src="https://calendly.com/helmsretirement/15min?hide_gdpr_banner=1" style="width:100%;height:100%;border:0" loading="lazy"></iframe>';
        }
        // Smooth scroll into view
        ty.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
})();

/* ===== Logo carousel ===== */
(function () {
  const carousels = document.querySelectorAll('.logo-carousel');
  if (!carousels.length) return;

  const AUTOSCROLL_MS = 2500;
  const STEP_ITEMS = 2; // how many logos to move per step

  carousels.forEach((wrap) => {
    const track = wrap.querySelector('.lc-track');
    const prev = wrap.querySelector('.lc-btn.prev');
    const next = wrap.querySelector('.lc-btn.next');
    if (!track || !prev || !next) return;

    // Lazy-load all carousel images for perf
    track.querySelectorAll('img').forEach((img) => (img.loading = 'lazy'));

    const getStep = () => {
      const item = track.querySelector('.lc-item');
      if (!item) return 180;
      const style = getComputedStyle(track);
      const gap = parseInt(style.columnGap || style.gap || '24', 10);
      return (item.getBoundingClientRect().width + gap) * STEP_ITEMS;
    };

    const stepScroll = (dir = 1) => {
      const step = getStep();
      track.scrollBy({ left: dir * step, behavior: 'smooth' });

      // Loop feeling at edges
      const nearEnd =
        track.scrollLeft + track.clientWidth >= track.scrollWidth - getStep();
      if (nearEnd && dir > 0) track.scrollTo({ left: 0 });
      const atStart = track.scrollLeft <= getStep();
      if (atStart && dir < 0) track.scrollTo({ left: track.scrollWidth });
    };

    prev.addEventListener('click', () => stepScroll(-1));
    next.addEventListener('click', () => stepScroll(1));

    // Auto-advance with polite behavior
    let timer;
    const start = () => {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      stop();
      timer = setInterval(() => stepScroll(1), AUTOSCROLL_MS);
    };
    const stop = () => timer && clearInterval(timer);

    // Pause on interaction
    wrap.addEventListener('mouseenter', stop);
    wrap.addEventListener('mouseleave', start);
    wrap.addEventListener('focusin', stop);
    wrap.addEventListener('focusout', start);
    wrap.addEventListener('touchstart', stop, { passive: true });
    wrap.addEventListener('touchend', start, { passive: true });

    // Kick off & handle tab visibility
    start();
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
  });
})();
