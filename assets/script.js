// ============ Logo carousel ============ //
(function () {
  const carousels = document.querySelectorAll('.logo-carousel');
  if (!carousels.length) return;

  const AUTOSCROLL_MS = 2500;
  const STEP_ITEMS = 2; // how many logos per click/advance

  carousels.forEach((wrap) => {
    const track = wrap.querySelector('.lc-track');
    const prev = wrap.querySelector('.lc-btn.prev');
    const next = wrap.querySelector('.lc-btn.next');
    if (!track || !prev || !next) return;

    // Determine step width from first items
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
      // if near end, jump back to start smoothly
      const nearEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - getStep();
      if (nearEnd && dir > 0) track.scrollTo({ left: 0 });
      const atStart = track.scrollLeft <= getStep();
      if (atStart && dir < 0) track.scrollTo({ left: track.scrollWidth });
    };

    prev.addEventListener('click', () => stepScroll(-1));
    next.addEventListener('click', () => stepScroll(1));

    // Auto-advance
    let timer;
    const start = () => {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      stop();
      timer = setInterval(() => stepScroll(1), AUTOSCROLL_MS);
    };
    const stop = () => timer && clearInterval(timer);

    // Pause on hover/focus/interaction
    wrap.addEventListener('mouseenter', stop);
    wrap.addEventListener('mouseleave', start);
    wrap.addEventListener('focusin', stop);
    wrap.addEventListener('focusout', start);
    wrap.addEventListener('touchstart', stop, { passive: true });
    wrap.addEventListener('touchend', start, { passive: true });

    // Kick off
    start();
    window.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
  });
})();
