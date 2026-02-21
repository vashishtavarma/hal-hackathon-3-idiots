# EduTube Chrome Extension

Opens a **side panel** when you click the extension icon. The panel is a self-contained app: sign in or sign up, then manage your **journeys** and **videos** (chapters). All data is stored in the EduTube backend (MongoDB).

## Flow

1. **Click extension icon** → Side panel opens.
2. **Not signed in** → Login form and a “Sign up” link to switch to the registration form.
3. **After sign in** → “Hi, &lt;name&gt;”, list of your journeys, **Create journey**, and a **Delete** button on each journey.
4. **Click a journey** → List of videos (chapters) in a scrollable area, **Add video**, and **Delete** on each video. Clicking a video title opens the video URL in a new tab.
5. **Sign out** → Returns to the login view.

All create/delete actions call the EduTube API; changes are persisted in MongoDB.

## Setup

1. **Backend**  
   Run the EduTube API (e.g. `http://localhost:5000`). The extension uses `http://localhost:5000/api/v1` by default (set in `sidepanel.js` as `API_BASE`).

2. **CORS**  
   If API requests fail with CORS errors, add your extension origin to the backend CORS allow list. In Chrome, get the extension ID from `chrome://extensions`, then allow `chrome-extension://&lt;YOUR_EXTENSION_ID&gt;` in the backend (e.g. in `main.py` or your CORS config).

3. **Icons**  
   Add PNGs to `icons/`: `icon16.png`, `icon48.png`, `icon128.png`.  
   See `icons/README.md`. Without them, Chrome may show a default icon.

4. **Load the extension**
   - Open `chrome://extensions`.
   - Turn on **Developer mode**.
   - Click **Load unpacked** and select the `edutube/extension` folder.

5. **Use it**
   - Pin the extension if needed (puzzle icon → pin EduTube).
   - Click the EduTube icon to open the side panel.

## Files

- `manifest.json` – Extension config (side panel, storage, host permissions).
- `sidepanel.html` – Panel layout (auth, dashboard, journey detail, modals).
- `sidepanel.css` – Styles for the panel.
- `sidepanel.js` – API client, auth, journeys, chapters (videos), and UI logic.
- `background.js` – Opens the side panel when the extension icon is clicked.
