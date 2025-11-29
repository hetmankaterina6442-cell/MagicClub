// reserved for future interactivity
// === Simple Lightbox ===
(function () {
  function ensureLightbox() {
    let lb = document.getElementById('lightbox');
    if (lb) return lb;
    lb = document.createElement('div');
    lb.id = 'lightbox';
    lb.innerHTML = `
      <div class="lb-backdrop"></div>
      <div class="lb-dialog">
        <img class="lb-image" alt="">
        <button class="lb-close" aria-label="Закрити">×</button>
      </div>`;
    document.body.appendChild(lb);
    return lb;
  }

  function openLightbox(src, alt) {
    const lb = ensureLightbox();
    lb.querySelector('.lb-image').src = src;
    lb.querySelector('.lb-image').alt = alt || '';
    lb.classList.add('open');
  }

  function closeLightbox() {
    const lb = document.getElementById('lightbox');
    if (lb) lb.classList.remove('open');
  }

  document.addEventListener('click', function (e) {
    const target = e.target.closest('.js-zoom');
    if (target) {
      e.preventDefault();
      const full = target.getAttribute('data-fullsrc') || target.src;
      openLightbox(full, target.alt);
    }
    if (e.target.matches('.lb-backdrop, .lb-close')) {
      closeLightbox();
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeLightbox();
  });
})();



