(function () {
  'use strict';

  document.documentElement.classList.add('js');

  function initOraculoPopup() {
    const popup = document.getElementById('oraculo-free-popup');
    if (!popup) return;

    const dialog = popup.querySelector('.oraculo-popup__dialog');
    const closeButtons = popup.querySelectorAll('[data-popup-close]');
    const cta = popup.querySelector('[data-popup-cta="oraculo-free"]');
    const displayDelayMs = 10 * 1000;
    let lastFocusedElement = null;
    let popupHasOpened = false;

    function closePopup() {
      if (popup.hidden) return;
      popup.hidden = true;
      document.body.classList.remove('oraculo-popup-open');

      if (lastFocusedElement instanceof HTMLElement) lastFocusedElement.focus();
    }

    function openPopup() {
      if (popupHasOpened) return;

      popupHasOpened = true;
      lastFocusedElement = document.activeElement;
      popup.hidden = false;
      document.body.classList.add('oraculo-popup-open');

      window.setTimeout(function () {
        if (dialog) dialog.focus();
      }, 0);
    }

    closeButtons.forEach(function (button) {
      button.addEventListener('click', closePopup);
    });
    if (cta) {
      cta.addEventListener('click', closePopup);
    }
    document.addEventListener('keydown', function (event) {
      if (popup.hidden) return;

      if (event.key === 'Escape') {
        closePopup();
        return;
      }

      if (event.key !== 'Tab' || !dialog) return;

      const focusableElements = Array.from(dialog.querySelectorAll(
        'button:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])'
      ));
      if (!focusableElements.length) {
        event.preventDefault();
        dialog.focus();
        return;
      }

      const firstFocusable = focusableElements[0];
      const lastFocusable = focusableElements[focusableElements.length - 1];
      if (event.shiftKey && (document.activeElement === firstFocusable || document.activeElement === dialog)) {
        event.preventDefault();
        lastFocusable.focus();
      } else if (!event.shiftKey && document.activeElement === lastFocusable) {
        event.preventDefault();
        firstFocusable.focus();
      }
    });

    window.setTimeout(openPopup, displayDelayMs);
    const canDetectExitIntent = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (canDetectExitIntent) {
      document.addEventListener('mouseout', function (event) {
        if (!event.relatedTarget && event.clientY <= 0) openPopup();
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initOraculoPopup);
  } else {
    initOraculoPopup();
  }
}());
