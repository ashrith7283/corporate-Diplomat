from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.app.schemas import TranslateRequest, TranslateResponse

router = APIRouter()

@router.get("/api/health")
async def health():
    return JSONResponse(content={"status": "ok"})

import asyncio
from fastapi import HTTPException
from backend.app.crew.diplomat_crew import crew

@router.post("/api/translate")
async def translate(req: TranslateRequest):
    try:
        result = await asyncio.wait_for(asyncio.to_thread(crew.kickoff, {"text": req.text, "direction": req.direction}), timeout=60.0)
        response = TranslateResponse(translated=result["translated"], notes=result.get("notes"))
        return response
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Translation request timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

