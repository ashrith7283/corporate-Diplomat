# Corporate Diplomat

## Overview

Corporate Diplomat is a tool designed to translate casual language into corporate jargon and vice versa. It uses a glossary of corporate terms combined with AI-powered translation agents to ensure accurate and clear communication within corporate environments.

## Features

- Translate casual text to corporate language and corporate language to casual text
- Utilize a static JSON corporate glossary for consistent terminology
- Two-agent CrewAI system for translation and style review
- Backend implemented with FastAPI and Python
- Frontend implemented with Angular and TailwindCSS
- Frontend and backend containerized separately and orchestrated via docker-compose

## Project Structure

```
corporate-diplomat/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── api/                   # API route handlers
│   │   ├── crew/                  # CrewAI agents and workflows
│   │   ├── schemas.py             # Pydantic models
│   │   ├── tools/                 # Helper tools like glossary
│   │   └── data/                  # Glossary JSON and other data
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── environments/          # Angular environment configs
│   │   └── app/                   # Components, services, models
│   ├── nginx.conf                 # SPA + reverse proxy for /api
│   ├── Dockerfile
│   └── .dockerignore
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── PLAN.md
└── README.md
```

## Getting Started

### Prerequisites

- Docker and Docker Compose (for the recommended setup), **or**:
  - Python 3.11+
  - Node.js 20+ and npm
- An OpenAI API key

### Option 1 — Run with Docker (recommended)

The frontend and backend are containerized separately and orchestrated via docker-compose.

1. Copy the environment template and add your OpenAI API key:

```bash
cp .env.example .env
# Then edit .env and set OPENAI_API_KEY
```

2. Build and start both services:

```bash
docker compose up --build
```

3. Open the app:

- Frontend (Angular + nginx): http://localhost:4200
- Backend API (direct): http://localhost:8000
- Backend API (proxied through frontend): http://localhost:4200/api/*

API requests from the browser go to `/api/*` on the frontend and are reverse-proxied to the backend container, so there is no CORS issue in production.

To stop the stack:

```bash
docker compose down
```

Useful commands:

```bash
# Run in detached mode
docker compose up -d --build

# Tail logs from both services
docker compose logs -f

# Tail logs from just one service
docker compose logs -f backend
docker compose logs -f frontend

# Rebuild only the backend after code changes
docker compose build backend && docker compose up -d backend

# Rebuild only the frontend after code changes
docker compose build frontend && docker compose up -d frontend

# Stop and remove containers, networks, and the default images
docker compose down --rmi local
```

The glossary at `backend/data/glossary.json` is mounted read-only into the backend container, so editing it on the host takes effect after restarting the backend (`docker compose restart backend`) without rebuilding the image.

### Option 2 — Run locally without Docker

Use this when you want hot-reload on both ends.

#### Backend

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp backend/.env.example backend/.env
# Edit backend/.env and set OPENAI_API_KEY

uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm start
```

Then open http://localhost:4200. The Angular dev server proxies `/api/*` requests to `http://localhost:8000` only if you add a `proxy.conf.json`; otherwise the browser will hit the backend directly at `http://localhost:8000/api/*` (CORS is allowed for `http://localhost:4200` by default).

## Configuration

All runtime settings are read from environment variables. Docker Compose reads them from `.env` at the project root.

| Variable          | Default                                          | Description                                       |
| ----------------- | ------------------------------------------------ | ------------------------------------------------- |
| `OPENAI_API_KEY`  | _(required)_                                     | OpenAI API key used by the translation agent.    |
| `CORS_ORIGINS`    | `http://localhost,http://localhost:4200`         | Comma-separated list of allowed CORS origins.    |
| `FRONTEND_PORT`   | `4200`                                           | Host port the frontend (nginx) is published on.   |
| `BACKEND_PORT`    | `8000`                                           | Host port the backend (uvicorn) is published on.  |

## Usage

### Web UI

Open http://localhost:4200 and use the translator UI. Choose a direction (`casual_to_corporate` or `corporate_to_casual`), enter text, and submit.

### API endpoints

The backend exposes:

- `GET /api/health` — health check, returns `{"status": "ok"}`.
- `POST /api/translate` — translate text. Request body:

```json
{
  "text": "let's sync tomorrow and circle back",
  "direction": "casual_to_corporate"
}
```

Response body:

```json
{
  "translated": "We will convene a cross-functional alignment session tomorrow and iterate on the deliverable.",
  "notes": "Replaced casual phrasing with formal corporate terminology."
}
```

`direction` must be either `casual_to_corporate` or `corporate_to_casual`.

Example with curl:

```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "let'\''s sync tomorrow", "direction": "casual_to_corporate"}'
```

## Contributing

Contributions are welcome. Please open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License.
