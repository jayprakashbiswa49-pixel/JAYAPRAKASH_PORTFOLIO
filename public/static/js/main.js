/**
 * Neumorphic Portfolio Interactive Engine
 * Developer: Jayaprakash Biswal
 * Features: Accessible mobile drawer, Scroll Spy, Project Category Filter, AJAX Contact Handler
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNavigation();
  initScrollSpy();
  initProjectFiltering();
  initContactForm();
  initBackToTop();
});

/**
 * Mobile Navigation Drawer Toggle & ARIA synchronization
 */
function initMobileNavigation() {
  const toggleBtn = document.getElementById('mobileNavToggle');
  const drawer = document.getElementById('mobileDrawer');
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');

  if (!toggleBtn || !drawer) return;

  function toggleMenu(forceClose = false) {
    const isCurrentlyOpen = toggleBtn.classList.contains('open');
    const shouldOpen = forceClose ? false : !isCurrentlyOpen;

    toggleBtn.classList.toggle('open', shouldOpen);
    drawer.classList.toggle('open', shouldOpen);
    toggleBtn.setAttribute('aria-expanded', shouldOpen ? 'true' : 'false');
  }

  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleMenu();
  });

  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      toggleMenu(true);
    });
  });

  document.addEventListener('click', (e) => {
    if (drawer.classList.contains('open') && !drawer.contains(e.target) && !toggleBtn.contains(e.target)) {
      toggleMenu(true);
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('open')) {
      toggleMenu(true);
      toggleBtn.focus();
    }
  });
}

/**
 * Scroll Spy for Active Navigation Link Highlighting
 */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const desktopLinks = document.querySelectorAll('.nav-link');
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');

  if (!sections.length) return;

  const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -60% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        updateActiveNav(id);
      }
    });
  }, observerOptions);

  sections.forEach(section => observer.observe(section));

  function updateActiveNav(activeId) {
    desktopLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href === `#${activeId}`) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    mobileLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href === `#${activeId}`) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }
}

/**
 * Project Category Filter Tabs
 */
function initProjectFiltering() {
  const filterButtons = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');

  if (!filterButtons.length || !projectCards.length) return;

  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active button state
      filterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      projectCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        if (filterValue === 'all' || cardCategory === filterValue) {
          card.style.display = 'flex';
          card.style.opacity = '1';
        } else {
          card.style.display = 'none';
          card.style.opacity = '0';
        }
      });
    });
  });
}

/**
 * Asynchronous AJAX Contact Form Submission
 */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
  const initialBtnText = submitBtn ? submitBtn.innerHTML : 'Send Message';

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Client-side quick check
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const subjectInput = document.getElementById('subject');
    const messageInput = document.getElementById('message');
    const honeypot = document.getElementById('hp_website');

    clearFormErrors();

    let hasErrors = false;
    if (!nameInput.value.trim() || nameInput.value.trim().length < 2) {
      showFieldError(nameInput, 'Name must be at least 2 characters.');
      hasErrors = true;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailInput.value.trim() || !emailRegex.test(emailInput.value.trim())) {
      showFieldError(emailInput, 'Please provide a valid email address.');
      hasErrors = true;
    }

    if (!subjectInput.value.trim() || subjectInput.value.trim().length < 3) {
      showFieldError(subjectInput, 'Subject must be at least 3 characters.');
      hasErrors = true;
    }

    if (!messageInput.value.trim() || messageInput.value.trim().length < 10) {
      showFieldError(messageInput, 'Message must be at least 10 characters.');
      hasErrors = true;
    }

    if (hasErrors) return;

    // Retrieve CSRF token
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : '';

    const payload = {
      name: nameInput.value.trim(),
      email: emailInput.value.trim(),
      subject: subjectInput.value.trim(),
      message: messageInput.value.trim(),
      hp_website: honeypot ? honeypot.value : '',
      csrf_token: csrfToken
    };

    // UI Loading state
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="animation: spin 1s linear infinite;">
          <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
          <path d="M12 2 A10 10 0 0 1 22 12"></path>
        </svg>
        <span>Sending...</span>
      `;
    }

    try {
      const response = await fetch('/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showToast(result.message || 'Thank you! Your message has been sent.', 'success');
        form.reset();
      } else {
        if (result.errors) {
          for (const [field, messages] of Object.entries(result.errors)) {
            const input = document.getElementById(field);
            if (input) showFieldError(input, messages[0]);
          }
        }
        showToast(result.message || 'There were errors with your submission. Please check the fields.', 'danger');
      }
    } catch (err) {
      showToast('Network error while sending message. Please try again or email directly.', 'danger');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = initialBtnText;
      }
    }
  });

  function showFieldError(inputElem, message) {
    const group = inputElem.closest('.form-group');
    if (!group) return;
    let errorElem = group.querySelector('.form-error');
    if (!errorElem) {
      errorElem = document.createElement('div');
      errorElem.className = 'form-error';
      group.appendChild(errorElem);
    }
    errorElem.textContent = message;
    inputElem.setAttribute('aria-invalid', 'true');
  }

  function clearFormErrors() {
    const errors = form.querySelectorAll('.form-error');
    errors.forEach(e => e.remove());
    const inputs = form.querySelectorAll('.form-control');
    inputs.forEach(i => i.removeAttribute('aria-invalid'));
  }
}

/**
 * Toast Notification Dispatcher
 */
function showToast(message, type = 'success') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.setAttribute('role', 'alert');

  toast.innerHTML = `
    <span>${message}</span>
    <button type="button" class="toast-close" aria-label="Close notification">&times;</button>
  `;

  toast.querySelector('.toast-close').addEventListener('click', () => {
    toast.remove();
  });

  container.appendChild(toast);

  // Auto-dismiss after 6 seconds
  setTimeout(() => {
    if (toast.parentNode) {
      toast.style.transition = 'opacity 300ms, transform 300ms';
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }
  }, 6000);
}

/**
 * Back to top smooth scroll
 */
function initBackToTop() {
  const backToTopBtn = document.getElementById('backToTopBtn');
  if (!backToTopBtn) return;

  backToTopBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

// Keyframe animation for inline spinner
const style = document.createElement('style');
style.textContent = `
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);
