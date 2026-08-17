# Corporate Diplomat — Build Plan

## Idea Rating: 8/10

**Strengths:** Solves a real, relatable pain point (corporate jargon decoding is genuinely useful for new employees, cross-functional teams, and external partners). Clear scope, demo-friendly, and CrewAI's multi-agent design maps naturally to the bidirectional translation. The niche is specific enough to differentiate from generic "rewrite this" tools.

**Risks:** Competitive space (rewording tools exist), so differentiation must come from the corporate-specific glossary and agentic reasoning. Keep MVP tight.

---

## Stack
- **Frontend:** Angular 17+ (standalone components, signals), TailwindCSS
- **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic v2
- **Agent Framework:** CrewAI with OpenAI GPT-4o-mini
- **Tool:** Static JSON corporate glossary
- **Local dev only** — no Docker

---

## Architecture
```
Angular SPA (4200)  ──HTTP──▶  FastAPI (8000)  ──▶  CrewAI Crew
   │                              │                     │
   │                              │                ┌────┴────────┐
   │                              │                │ Translator  │ (direction-aware)
   │                              │                │ Reviewer    │
   │                              │                └─────────────┘
   │                              ▼
   │                       JSON response
   ▼
  Modern button UI
```

---

## Crew Design (2 agents — kept lean per MVP scope)
1. **Diplomat Translator** — role-conditional: rewrites *casual → corporate* OR *corporate → casual* based on a `direction` input. Uses the glossary tool for consistent terminology.
2. **Style Reviewer** — verifies tone accuracy and clarity, returns final version with optional `notes` explaining tricky terms.

Sequential process: `Translator → Reviewer`.

**Agent rationale:** Two agents (not three) keeps latency low and cost minimal while preserving the "agentic" feel. The Reviewer catches hallucinations and tone drift, which is the main value-add over a single prompt.

---

## UI (Angular) — Single screen
- **Mode toggle:** two pill buttons — "Casual → Corporate" / "Corporate → Casual" (default: Casual → Corporate)
- **Input textarea** (left/top)
- **↔ Swap button** — swaps mode + moves output to input
- **Output textarea** (read-only) + **Copy** icon button
- **Translate button** (primary CTA, disabled while loading)
- **Error toast** for API failures

Clean modern aesthetic: rounded corners, soft shadows, neutral palette with one accent color.

---

## API Contract
```
POST /api/translate
Request:  { "text": "string", "direction": "casual_to_corporate" | "corporate_to_casual" }
Response: { "translated": "string", "notes": "string?" }

GET /api/health  →  { "status": "ok" }
```
CORS: `http://localhost:4200`.

---

## Project Structure
```
corporate-diplomat/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app + CORS
│   │   ├── api/routes.py           # /api/translate, /api/health
│   │   ├── schemas.py              # Pydantic models
│   │   ├── crew/
│   │   │   ├── diplomat_crew.py    # Crew() wiring
│   │   │   ├── agents.py           # translator + reviewer agents
│   │   │   └── tasks.py            # direction-aware tasks
│   │   └── tools/
│   │       └── glossary.py         # JSON glossary tool
│   ├── data/
│   │   └── glossary.json           # ~60 common corp terms
│   ├── requirements.txt
│   └── .env                        # OPENAI_API_KEY
└── frontend/
    └── src/app/
        ├── components/
        │   ├── translator/         # main shell
        │   ├── mode-toggle/
        │   ├── text-panel/
        │   └── swap-button/
        ├── services/translate.service.ts
        └── app.config.ts
```

---

## Implementation Phases

**Phase 1 — Backend skeleton**
- `uvicorn` runs, `/health` returns ok, `/api/translate` returns stub.
- Pydantic schemas defined.

**Phase 2 — Glossary tool**
- Curate `glossary.json` (~60 terms) with plain-English meanings.
- Wrap as a CrewAI `BaseTool` that agents can query.

**Phase 3 — Crew**
- `agents.py`: 2 agents with role/goal/backstory tuned for corporate tone.
- `tasks.py`: 2 tasks with `output_pydantic` for structured results.
- `diplomat_crew.py`: `Crew(agents, tasks, process=sequential)`.
- Smoke test with 3 sample inputs each direction.

**Phase 4 — Wire route → crew**
- `/api/translate` calls `crew.kickoff(inputs={...})`, returns JSON.
- 60s timeout, friendly error messages.

**Phase 5 — Angular UI**
- Standalone `TranslatorComponent`, signals for `mode`, `inputText`, `outputText`, `loading`, `error`.
- `TranslateService.translate(text, direction)` → HTTP POST.
- Tailwind for styling.

**Phase 6 — Polish**
- Copy-to-clipboard, swap button (moves output→input + flips mode), disable button on empty input, loading spinner on CTA.

---

## Glossary Tool Spec (sample)
```json
{
  "terms": {
    "circle back": "discuss again later",
    "low-hanging fruit": "easy wins",
    "move the needle": "create meaningful progress",
    "bandwidth": "available capacity",
    "synergy": "combined effect greater than the sum of parts",
    "boil the ocean": "try to do everything at once (avoid)",
    "deep dive": "detailed analysis",
    "open the kimono": "share full information transparently",
    "touch base": "briefly connect or check in",
    "take this offline": "discuss privately outside the meeting",
    "net-net": "the bottom-line conclusion",
    "value-add": "something extra of benefit",
    "drill down": "examine in more detail",
    "pivot": "change strategy or direction",
    "right-size": "adjust to the appropriate scale",
    "stakeholder": "anyone affected by or influencing the outcome",
    "deliverable": "a tangible output or result",
    "action item": "a task assigned to someone",
    "best practice": "a proven method that works well",
    "pain point": "a specific problem or frustration",
    "win-win": "an outcome where both sides benefit",
    "table this": "postpone discussion for later",
    "parking lot": "a place to park ideas for later discussion",
    "granular": "detailed to a fine level",
    "holistic": "considering the whole picture",
    "leverage": "use to maximum advantage",
    "optimize": "make as effective as possible",
    "streamline": "simplify and improve efficiency",
    "ideate": "generate ideas",
    "incentivize": "provide motivation to act",
    "monetize": "convert into revenue",
    "operationalize": "put into active use",
    "productize": "turn into a repeatable product",
    "scale": "grow or expand",
    "socialize": "share informally for feedback",
    "synergize": "combine for greater effect",
    "unpack": "explain in detail",
    "workstream": "a stream of related work",
    "bandwidth": "available time and capacity",
    "blocker": "something preventing progress",
    "boots on the ground": "people actively doing the work",
    "buckets": "categories or groupings",
    "buy-in": "agreement or support",
    "cadence": "regular rhythm of meetings or updates",
    "core competency": "a key area of expertise",
    "crunch time": "period of intense effort before a deadline",
    "deep work": "focused, uninterrupted work",
    "disrupt": "fundamentally change an industry",
    "double-click": "look at something more closely",
    "ducks in a row": "things organized and in order",
    "elevator pitch": "a brief summary of an idea",
    "executive summary": "a concise overview for leaders",
    "fast follower": "a company that copies a market leader",
    "go-to-market": "the strategy for launching a product",
    "headcount": "number of employees",
    "heavy lifting": "the most difficult work",
    "in the weeds": "lost in too much detail",
    "kick off": "start a project or meeting",
    "learnings": "insights gained from experience",
    "level set": "establish shared understanding",
    "move the goalposts": "change the criteria after the fact",
    "on the same page": "in agreement",
    "out of pocket": "unavailable or unreachable",
    "parity": "equal level or status",
    "quick win": "an easy, fast achievement",
    "RACI": "responsible, accountable, consulted, informed",
    "runway": "available time or resources before a deadline",
    "single source of truth": "the authoritative data source",
    "SLA": "service level agreement",
    "smoke test": "a basic test to see if something works",
    "straw man": "a simplified version of an idea to argue against",
    "sustainability": "ability to maintain over time",
    "SWOT": "strengths, weaknesses, opportunities, threats",
    "thought leadership": "being seen as an authority on a topic",
    "top of mind": "the first thing people think of",
    "value proposition": "the unique benefit offered",
    "vertical": "a specific industry or market"
  }
}
```

Tool returns matching terms when agents detect them in input.

---

## Verification Checklist
- [ ] `curl POST /api/translate` returns valid translation each direction
- [ ] Glossary terms appear in `corporate → casual` output
- [ ] Angular renders, button toggles mode, swap works, copy works
- [ ] Error shown when API key missing or network fails
- [ ] Loading state visible during ~2-5s LLM call

---

## Quick Start (after implementation)

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm start   # serves on http://localhost:4200
```
