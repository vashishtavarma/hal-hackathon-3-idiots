/**
 * Popup script: read/write focus mode preference and sync with content script.
 */
const FOCUS_MODE_KEY = 'hal_focus_mode';

const checkbox = document.getElementById('focusMode');

// Load saved preference
chrome.storage.local.get([FOCUS_MODE_KEY], (result) => {
  checkbox.checked = result[FOCUS_MODE_KEY] === true;
});

// Persist and notify content script when toggled
checkbox.addEventListener('change', () => {
  const enabled = checkbox.checked;
  chrome.storage.local.set({ [FOCUS_MODE_KEY]: enabled }, () => {
    // Tell any open YouTube tab to apply or remove focus mode
    chrome.tabs.query({ url: 'https://www.youtube.com/*' }, (tabs) => {
      tabs.forEach((tab) => {
        chrome.tabs.sendMessage(tab.id, { action: 'focusMode', enabled }).catch(() => {});
      });
    });
  });
});
