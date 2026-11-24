"""ResearchGuard Vercel FastAPI: public read-only sources + authenticated AI operators."""
from __future__ import annotations
import hmac
import json
import os
from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from core import SERVICES, run
from transport import SourceError
from agent_console import CONSOLE_HTML
from agent_engine import AgentError, orchestrate, configured, credit_balance, MODEL

app = FastAPI(
    title="MUHRIS ResearchGuard — Multi-agent Evidence Studio",
    description="Public Crossref discovery plus operator-authorized, model-metered multi-agent analysis.",
    version="0.2.0"
)

class AgentQuery(BaseModel):
    topic: str = Field(min_length=3, max_length=120)

def _require_operator(authorization: str | None):
    """Never permit a public request to spend project LLM credits."""
    expected = os.environ.get("AGENT_ACCESS_TOKEN", "")
    if len(expected) < 24 or os.environ.get("AI_AGENT_ENABLED") != "1":
        raise HTTPException(503, "Private AI-agent operations are not yet activated by the project owner.")
    supplied = (authorization or "")
    if not supplied.startswith("Bearer ") or not hmac.compare_digest(supplied[7:], expected):
        raise HTTPException(401, "Operator authorization required.")
    if not configured():
        raise HTTPException(503, "AI Gateway OIDC or API key is not configured.")

@app.get("/", response_class=HTMLResponse)
def home():
    return CONSOLE_HTML

@app.get("/health")
def health():
    return {"status":"ok", "projects":SERVICES,
            "data_access":"live Crossref; AI requires operator authorization",
            "ai_model_configured":configured(), "version":"0.2.0"}

@app.get("/api/agent-config")
def agent_config():
    return {"ai_enabled":configured(), "model":MODEL, "public_data":True,
            "requires_operator_token":True,"charges_from_public_requests":False,
            "estimate_only":True}

@app.get("/api")
def api(query: str = Query(min_length=2,max_length=120), service: str = ""):
    if service and service not in SERVICES:
        raise HTTPException(400,"Unknown project")
    try:
        return run(query,service or SERVICES[0])
    except ValueError as exc:
        raise HTTPException(400,str(exc)) from None
    except SourceError as exc:
        raise HTTPException(502,str(exc)) from None

@app.post("/api/agents")
def agents(request: AgentQuery, authorization: str | None = Header(default=None)):
    _require_operator(authorization)
    try:
        return orchestrate(request.topic)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from None
    except SourceError as exc:
        raise HTTPException(502, "Source API unavailable: " + str(exc)) from None
    except AgentError as exc:
        raise HTTPException(502, str(exc)) from None

@app.get("/api/credits")
def credits(authorization: str | None = Header(default=None)):
    _require_operator(authorization)
    try:
        return credit_balance()
    except AgentError as exc:
        raise HTTPException(502, str(exc)) from None
