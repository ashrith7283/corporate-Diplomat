# Corporate Diplomat

## Overview

Corporate Diplomat is a tool designed to translate casual language into corporate jargon and vice versa. It uses a glossary of corporate terms combined with AI-powered translation agents to ensure accurate and clear communication within corporate environments.

## Features

- Translate casual text to corporate language and corporate language to casual text
- Utilize a static JSON corporate glossary for consistent terminology
- Two-agent CrewAI system for translation and style review
- Backend implemented with FastAPI and Python
- Frontend planned with Angular and TailwindCSS

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
│   │   ├── data/                  # Glossary JSON and other data
│   │   └── .env                  # Environment variables (e.g., API keys)
├── frontend/                     # Frontend Angular app (planned)
├── PLAN.md                      # Project build and implementation plan
└── README.md                    # This file
```

## Getting Started

### Prerequisites

- Python 3.11+
- OpenAI API Key

### Setup Backend

1. Navigate to the backend directory:

```bash
cd backend
```

2. Install dependencies (including uvloop):

```bash
python3 -m pip install -r requirements.txt uvloop
```

3. Copy `.env` and add your OpenAI API Key:

```bash
cp .env.example .env
# Then edit .env to add your key
```

4. Run the backend server (with uvloop enabled):

```bash
python3 -m uvicorn backend.app.main:app --reload
```

## Usage

- Access the API endpoints:
  - `GET /api/health` to check server status
  - `POST /api/translate` with JSON body `{ "text": "", "direction": "casual_to_corporate" | "corporate_to_casual" }`

## Contributing

Contributions are welcome! Please open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License.
