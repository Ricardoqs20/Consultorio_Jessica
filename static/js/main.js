// Smooth interactive interactions for FAQ accordion and navigation
document.addEventListener('DOMContentLoaded', () => {
  // FAQ Accordion
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach((item) => {
    const header = item.querySelector('.faq-header');
    header.addEventListener('click', () => {
      const isActive = item.classList.contains('active');

      // Close all other open items
      faqItems.forEach((other) => {
        other.classList.remove('active');
        const icon = other.querySelector('.faq-icon');
        if (icon) icon.textContent = '+';
      });

      // Toggle current
      if (!isActive) {
        item.classList.add('active');
        const icon = item.querySelector('.faq-icon');
        if (icon) icon.textContent = '−';
      }
    });
  });

  // Google Reviews Carousel Navigation
  const track = document.getElementById('reviewsTrackContainer');
  const prevBtn = document.getElementById('revPrevBtn');
  const nextBtn = document.getElementById('revNextBtn');

  if (track && prevBtn && nextBtn) {
    const scrollStep = 300; // card width + gap

    prevBtn.addEventListener('click', () => {
      track.scrollBy({ left: -scrollStep, behavior: 'smooth' });
    });

    nextBtn.addEventListener('click', () => {
      track.scrollBy({ left: scrollStep, behavior: 'smooth' });
    });
  }

  // Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.length > 1) {
        e.preventDefault();
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });
  // PWA Configuration: Only register Service Worker on Mobile devices (Android / iOS)
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) 
                   || (navigator.maxTouchPoints > 1 && window.innerWidth <= 1024);

  // Prevent desktop browser from showing the "Install App" / "Baixar aplicativo" prompt in omnibox/address bar
  window.addEventListener('beforeinstallprompt', (e) => {
    if (!isMobile) {
      e.preventDefault(); // Suppress install banner / button on PC
      return false;
    }
  });

  // Register Service Worker for PWA (Active on mobile for offline and installable web app)
  if (isMobile && 'serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .then((reg) => {
          console.log('[PWA Mobile] Service Worker registrado com sucesso:', reg.scope);
        })
        .catch((err) => {
          console.log('[PWA Mobile] Falha ao registrar Service Worker:', err);
        });
    });
  } else if (!isMobile && 'serviceWorker' in navigator) {
    // Unregister any active service worker on desktop if previously registered
    navigator.serviceWorker.getRegistrations().then((registrations) => {
      for (const registration of registrations) {
        registration.unregister();
      }
    });
  }

  // Mobile Navigation Drawer Toggle
  const mobileToggle = document.getElementById('mobileNavToggle');
  const navWrapper = document.getElementById('navWrapper');

  if (mobileToggle && navWrapper) {
    mobileToggle.addEventListener('click', () => {
      mobileToggle.classList.toggle('open');
      navWrapper.classList.toggle('open');
      document.body.style.overflow = navWrapper.classList.contains('open') ? 'hidden' : '';
    });

    // Close mobile menu on clicking any navigation link
    navWrapper.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        mobileToggle.classList.remove('open');
        navWrapper.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }
});
