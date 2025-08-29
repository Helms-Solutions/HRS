// Year stamp
document.getElementById('yr') && (document.getElementById('yr').textContent = new Date().getFullYear());

// Add current query string to Calendly links (UTMs carry through)
const qs = window.location.search || '';
document.querySelectorAll('[data-calendly]').forEach(a => {
  try { const u = new URL(a.href); a.href = u.origin + u.pathname + qs; } catch {}
});

// On lead form submit → reveal inline Calendly
document.querySelectorAll('form.js-lead').forEach(form => {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const ty = document.getElementById('thankyou');
    if (ty) {
      ty.hidden = false;
      const w = document.getElementById('calendly-inline-widget');
      if (w) w.setAttribute('data-url', 'https://calendly.com/helmsretirement/15min' + qs);
      ty.scrollIntoView({behavior:'smooth'});
    }
  });
});
