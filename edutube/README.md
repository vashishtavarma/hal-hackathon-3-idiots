# EduTube

Transform YouTube into a focused, interactive learning environment: reduce distractions and add notes, AI assistance, quizzes, and collaboration (without modifying YouTube itself).

## Tech stack

| Layer     | Stack                 |
|-----------|------------------------|
| Backend   | FastAPI                |
| Frontend  | React (Vite)           |
| Database  | MongoDB                |
| Extension | HTML, CSS, JavaScript  |

## Project layout

```
edutube/
├── backend/     # EduTube API (FastAPI + MongoDB) — see backend/README.md
├── frontend/    # React (Vite)
├── extension/   # Browser extension (HTML/CSS/JS)
└── README.md
```

## Quick start

### 1. Backend (FastAPI + MongoDB)

- Python 3.11+
- MongoDB running (local or Atlas)

From the **edutube** directory:

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: MONGODB_URL, JWT_SECRET, etc.
```

Run the server (default port 5000):

```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```

- API base: `http://localhost:5000/api/v1`
- Docs: `http://localhost:5000/docs`

Full API details: [backend/README.md](backend/README.md).

### 2. Frontend (React)

From the **edutube** directory:

```bash
cd frontend
npm install
npm run dev
```

- App: http://localhost:5173  
- Ensure the frontend proxy target in `vite.config.js` matches the backend port (e.g. 5000).

### 3. Extension

- Add toolbar icons in `extension/icons/`: `icon16.png`, `icon48.png`, `icon128.png` (see [extension/icons/README.md](extension/icons/README.md)).
- In Chrome: `chrome://extensions` → **Developer mode** → **Load unpacked** → select `edutube/extension`.

## What’s included

- **Backend**: EduTube API — users, journeys, chapters, notes, chatbot. FastAPI + MongoDB, CORS enabled for frontend and extension.
- **Frontend**: Vite + React, signup/login, home; proxies `/api` to backend.
- **Extension**: Focus mode toggle; content script hides YouTube secondary column and Shorts when enabled.

## E2E check

With backend and frontend running:

1. Open http://localhost:5173/signup and create an account.
2. After signup you are redirected to home.
3. Home shows **Hi, &lt;your name&gt;** when logged in.
4. Or use http://localhost:5173/auth to sign in.
