/* ================================================================
   Connected Development [CODE] — main.js
   Handles: nav scroll, hero slider, scroll reveal, counters,
            mobile nav, footer newsletter AJAX, scroll-to-top
   ================================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ── NAV SCROLL DARKEN ── */
  const nav = document.getElementById('main-nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.style.background = window.scrollY > 80
        ? 'rgba(0,21,21,0.99)'
        : 'rgba(0,37,37,0.97)';
    });
  }

  /* ── SCROLL-TO-TOP BUTTON ── */
  const scrollTopBtn = document.getElementById('scrollTop');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      scrollTopBtn.classList.toggle('show', window.scrollY > 500);
    });
  }

  /* ── MOBILE NAV ── */
  const hamburger = document.getElementById('navHamburger');
  const mobileNav = document.getElementById('mobileNav');
  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      mobileNav.classList.toggle('open');
    });
    // Close on link click
    mobileNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        hamburger.classList.remove('open');
        mobileNav.classList.remove('open');
      });
    });
  }

  /* ── HERO SLIDER ── */
  const slides = document.querySelectorAll('.slide');
  const dotsContainer = document.getElementById('sliderDots');

  if (slides.length > 0 && dotsContainer) {
    // Build dots
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'dot' + (i === 0 ? ' active' : '');
      dot.dataset.i = i;
      dot.addEventListener('click', () => goTo(i));
      dotsContainer.appendChild(dot);
    });

    let current = 0;
    let timer;

    function goTo(i) {
      slides[current].classList.remove('active');
      dotsContainer.children[current].classList.remove('active');
      current = (i + slides.length) % slides.length;
      slides[current].classList.add('active');
      dotsContainer.children[current].classList.add('active');
      resetTimer();
    }

    function resetTimer() {
      clearInterval(timer);
      timer = setInterval(() => goTo(current + 1), 6000);
    }

    const prevBtn = document.getElementById('prev');
    const nextBtn = document.getElementById('next');
    if (prevBtn) prevBtn.addEventListener('click', () => goTo(current - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => goTo(current + 1));

    resetTimer();
  }

  /* ── SCROLL REVEAL ── */
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll(
    '.fade-up, .reveal, .stat-card, .mandate-card, .value-item, ' +
    '.thematic-card, .story-card, .vm-card, .obj-card, .post-card, ' +
    '.featured-post, .related-card'
  ).forEach(el => revealObserver.observe(el));

  /* ── COUNTER ANIMATION ── */
  function animateCount(el, target, suffix) {
    let val = 0;
    const step = target / 60;
    const interval = setInterval(() => {
      val += step;
      if (val >= target) {
        val = target;
        clearInterval(interval);
      }
      el.textContent = Math.floor(val) + suffix;
    }, 22);
  }

  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting && !e.target.dataset.counted) {
        e.target.dataset.counted = '1';
        e.target.querySelectorAll('[data-target]').forEach(numEl => {
          const target = parseInt(numEl.dataset.target);
          const suffix = numEl.dataset.suffix || '+';
          animateCount(numEl, target, suffix);
        });
        // Also handle stat-number spans on homepage
        e.target.querySelectorAll('.stat-number').forEach(numEl => {
          const text = numEl.textContent;
          const match = text.match(/(\d+)/);
          if (match) {
            const target = parseInt(match[1]);
            const suffix = text.replace(/\d+/, '');
            numEl.textContent = '0' + suffix;
            animateCount({ set textContent(v) { numEl.textContent = v; } }, target, suffix);

            // Actually do it properly
            let val = 0;
            const step = target / 60;
            const span = numEl.querySelector('span');
            const interval = setInterval(() => {
              val += step;
              if (val >= target) { val = target; clearInterval(interval); }
              numEl.childNodes[0].textContent = Math.floor(val);
            }, 22);
          }
        });
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.about-stats, .visual-card').forEach(el => countObserver.observe(el));

  /* ── STAGGER THEMATIC CARDS ── */
  document.querySelectorAll('.thematic-card').forEach((c, i) => {
    if (!c.style.transitionDelay) {
      c.style.transitionDelay = (i * 0.08) + 's';
    }
  });

  /* ── FOOTER NEWSLETTER AJAX ── */
  const footerForm = document.getElementById('footerNewsletterForm');
  const footerMsg  = document.getElementById('footerNewsletterMsg');

  if (footerForm) {
    footerForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const data = new FormData(footerForm);

      fetch(footerForm.action, {
        method: 'POST',
        body: data,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(r => r.json())
        .then(json => {
          if (footerMsg) {
            footerMsg.textContent = json.message;
            footerMsg.style.color = json.status === 'ok' ? 'var(--gold-light)' : 'rgba(255,255,255,0.7)';
            footerMsg.style.fontSize = '12px';
            footerMsg.style.marginTop = '8px';
          }
          if (json.status === 'ok') footerForm.reset();
        })
        .catch(() => {
          if (footerMsg) footerMsg.textContent = 'Something went wrong. Please try again.';
        });
    });
  }

  /* ── DISMISS DJANGO MESSAGES ── */
  setTimeout(() => {
    document.querySelectorAll('.django-message').forEach(el => {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    });
  }, 4000);

});
