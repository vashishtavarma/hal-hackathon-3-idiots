# EduTube — Backend API

Backend for **EduTube**: learning journeys, chapters, notes, and an AI chatbot. FastAPI + MongoDB. See [edutube/README.md](../README.md) for full project setup.

## Requirements

- Python 3.11+
- MongoDB (local or Atlas)

## Setup

1. **Create a virtualenv and install dependencies**

   ```bash
   # From edutube repo root
   cd backend
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # Unix: source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment**

   Copy `.env.example` to `.env` and set:

   - `JWT_SECRET` — secret for JWT auth
   - `MONGODB_URL` — e.g. `mongodb://localhost:27017` or your Atlas URI
   - Optionally `GEMINI_API_KEY`, `YT_KEY` for chatbot and YouTube playlist import

3. **Run the server**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 5000
   ```

   Or use the port from your `.env` (e.g. `PORT=5000`).

## API

- **Base path:** `/api/v1`
- **Auth:** `Authorization: Bearer <token>` (JWT from `/api/v1/users/login`)
- **Users:** `POST /users/register`, `POST /users/login`, `GET /users/profile`, `GET /users`
- **Journeys:** `GET/POST /journeys`, `GET/PUT/DELETE /journeys/:id`, `POST /journeys/playlist`, `POST /journeys/:id/fork`, `GET /journeys/public`
- **Chapters:** `GET/POST /journeys/:journeyId/chapters`, `GET/PUT/DELETE /journeys/chapters/:id`, `PUT /journeys/chapters/isComplete/:id`
- **Notes:** `GET/POST .../chapters/:chapterId/notes`, `GET /journeys/:journeyId/notes`, `GET/PUT/DELETE /notes/:noteId`
- **Chatbot:** `POST /chatbot/chat`, `GET /chatbot/health`

Point the frontend at this server (e.g. `http://localhost:5000/api/v1`).
