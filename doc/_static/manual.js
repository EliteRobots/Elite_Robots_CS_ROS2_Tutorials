// Navigation and small progressive enhancements; Sphinx owns full-text search.
document.addEventListener('DOMContentLoaded', () => {
  const menu = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.chapter-sidebar');
  const setOpen = (open) => {
    document.body.classList.toggle('nav-open', open);
    menu?.setAttribute('aria-expanded', String(open));
  };
  menu?.addEventListener('click', () => setOpen(menu.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && document.body.classList.contains('nav-open')) {
      setOpen(false); menu.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!sidebar?.contains(event.target) && !menu?.contains(event.target)) setOpen(false);
  });
  sidebar?.querySelectorAll('nav a').forEach((link) => link.addEventListener('click', () => setOpen(false)));
  document.querySelectorAll('.chapter-tree a.current').forEach((link) => link.setAttribute('aria-current', 'page'));
  document.querySelectorAll('.body .highlight').forEach((block) => {
    const pre = block.querySelector('pre');
    if (!pre) return;
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'copy-code';
    button.textContent = document.body.dataset.copyLabel;
    button.setAttribute('aria-live', 'polite');
    button.addEventListener('click', async () => {
      const text = pre.textContent;
      try {
        if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(text);
        else {
          const input = document.createElement('textarea');
          input.value = text; input.style.cssText = 'position:fixed;left:-9999px;top:0';
          document.body.append(input); input.select();
          let copied;
          try { copied = document.execCommand('copy'); } finally { input.remove(); button.focus(); }
          if (!copied) throw new Error('Copy unavailable');
        }
        button.textContent = document.body.dataset.copiedLabel;
      } catch (_) { button.textContent = document.body.dataset.copyFailedLabel; }
      window.setTimeout(() => { button.textContent = document.body.dataset.copyLabel; }, 2000);
    });
    block.append(button);
  });
  const links = [...document.querySelectorAll('.page-toc a[href^="#"]')];
  const headings = links.map((link) => {
    try { return {link, heading: document.getElementById(decodeURIComponent(link.hash.slice(1)))}; }
    catch (_) { return {link, heading: null}; }
  }).filter((item) => item.heading);
  let pending = false;
  const updateToc = () => {
    let active = headings[0];
    headings.forEach((item) => { if (item.heading.getBoundingClientRect().top <= 125) active = item; });
    headings.forEach((item) => {
      item.link.classList.toggle('active', item === active);
      if (item === active) item.link.setAttribute('aria-current', 'location');
      else item.link.removeAttribute('aria-current');
    });
    pending = false;
  };
  window.addEventListener('scroll', () => {
    if (!pending) { pending = true; window.requestAnimationFrame(updateToc); }
  }, {passive: true});
  updateToc();
});
