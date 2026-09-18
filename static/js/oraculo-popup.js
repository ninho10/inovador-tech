(function () {
  'use strict';

  document.documentElement.classList.add('js');

  function initOraculoPopup() {
    const popup = document.getElementById('oraculo-free-popup');
    if (!popup) return;

    const dialog = popup.querySelector('.oraculo-popup__dialog');
    const closeButtons = popup.querySelectorAll('[data-popup-close]');
    const cta = popup.querySelector('[data-popup-cta="oraculo-free"]');
    const dismissKey = 'oraculo_free_popup_dismissed_at';
    const shownKey = 'oraculo_free_popup_shown';
    const dismissWindowMs = 7 * 24 * 60 * 60 * 1000;
    let lastFocusedElement = null;
    let popupHasOpened = false;

    function wasDismissedRecently() {
      try {
        const dismissedAt = Number(localStorage.getItem(dismissKey));
        return Number.isFinite(dismissedAt) && Date.now() - dismissedAt < dismissWindowMs;
      } catch (error) {
        return false;
      }
    }

    function hasShownThisSession() {
      try {
        return sessionStorage.getItem(shownKey) === 'true';
      } catch (error) {
        return false;
      }
    }

    function closePopup(rememberDismissal) {
      if (popup.hidden) return;
      popup.hidden = true;
      document.body.classList.remove('oraculo-popup-open');

      if (rememberDismissal) {
        try {
          localStorage.setItem(dismissKey, String(Date.now()));
        } catch (error) {
          // Storage can be blocked; closing the popup must still work.
        }
      }

      if (lastFocusedElement instanceof HTMLElement) lastFocusedElement.focus();
    }

    function openPopup() {
      if (popupHasOpened || wasDismissedRecently() || hasShownThisSession()) return;

      popupHasOpened = true;
      lastFocusedElement = document.activeElement;
      popup.hidden = false;
      document.body.classList.add('oraculo-popup-open');

      try {
        sessionStorage.setItem(shownKey, 'true');
      } catch (error) {
        // The session guard remains best-effort when storage is unavailable.
      }

      window.setTimeout(function () {
        if (dialog) dialog.focus();
      }, 0);
    }

    closeButtons.forEach(function (button) {
      button.addEventListener('click', function () { closePopup(true); });
    });
    if (cta) {
      cta.addEventListener('click', function () { closePopup(false); });
    }
    document.addEventListener('keydown', function (event) {
      if (popup.hidden) return;

      if (event.key === 'Escape') {
        closePopup(true);
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

    if (wasDismissedRecently() || hasShownThisSession()) return;

    window.setTimeout(openPopup, 6500);
    const canDetectExitIntent = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (canDetectExitIntent) {
      document.addEventListener('mouseout', function (event) {
        if (!event.relatedTarget && event.clientY <= 0) openPopup();
      }, { once: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initOraculoPopup);
  } else {
    initOraculoPopup();
  }
}());
