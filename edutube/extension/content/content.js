/**
 * Content script for YouTube. Applies focus mode (hide recommendations, Shorts)
 * based on extension storage. Listens for messages from popup.
 */

const FOCUS_MODE_KEY = 'hal_focus_mode';
const BODY_CLASS = 'hal-focus-mode';

/**
 * Apply or remove focus mode by toggling a class on document body.
 */
function setFocusMode(enabled) {
  if (enabled) {
    document.body.classList.add(BODY_CLASS);
  } else {
    document.body.classList.remove(BODY_CLASS);
  }
}

/**
 * Load initial state from storage and apply focus mode.
 */
function init() {
  chrome.storage.local.get([FOCUS_MODE_KEY], (result) => {
    setFocusMode(result[FOCUS_MODE_KEY] === true);
  });
}

// Apply on load (e.g. user already had focus mode on)
init();

// React to popup toggles
chrome.runtime.onMessage.addListener((message) => {
  if (message.action === 'focusMode' && typeof message.enabled === 'boolean') {
    setFocusMode(message.enabled);
  }
});
