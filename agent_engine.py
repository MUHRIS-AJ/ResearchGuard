"""Real (opt-in) LLM agents: three independent model calls over real Crossref sources.

This is a private operator workflow. It never runs from an unauthenticated request.
Costs are estimates using a pinned model price; official billed spend lives at Vercel.
"""
from __future__ import annotations
import json
import os
import time
from dataclasses import dataclass, asdict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from core import discover
from transport import SourceError

GATEWAY = "https://ai-gateway.vercel.sh/v1"
MODEL = "google/gemini-2.5-flash-lite"
# Published Vercel AI Gateway catalog on 2026-11-24, USD per token, standard tier.
INPUT_PRICE = 0.00000010
OUTPUT_PRICE = 0.00000040
MAX_RUN_ESTIMATE_USD = 0.01
MAX_STEPS = 3

class AgentError(Exception):
    pass

def configured() -> bool:
    return bool(os.environ.get("AI_AGENT_ENABLED") == "1" and
                os.environ.get("AGENT_ACCESS_TOKEN") and
                (os.environ.get("AI_GATEWAY_API_KEY") or os.environ.get("VERCEL_OIDC_TOKEN")))

def _gateway_key():
    return os.environ.get("AI_GATEWAY_API_KEY") or os.environ.get("VERCEL_OIDC_TOKEN")

def _request(path: str, payload: dict | None = None):
    key = _gateway_key()
    if not key:
        raise AgentError("No Vercel Gateway credential. Configure OIDC or an AI Gateway API key.")
    headers = {"Authorization": "Bearer " + key, "Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    try:
        req = Request(GATEWAY + path, headers=headers, data=data,
                      method="POST" if data is not None else "GET")
        with urlopen(req, timeout=24) as res:
            raw = res.read(250_001)
        if len(raw) > 250_000:
            raise AgentError("Model response too large.")
        return json.loads(raw)
    except HTTPError as exc:
        # Never include headers, auth tokens or provider raw diagnostics.
        codes = {401: "Gateway authentication failed.",
                 402: "AI Gateway credits or spending limit exhausted.",
                 403: "Vercel requires billing verification or blocks access.",
                 429: "AI provider rate limit reached.",
                 503: "Provider temporarily unavailable."}
        raise AgentError(codes.get(exc.code, "AI Gateway HTTP " + str(exc.code))) from None
    except (URLError, TimeoutError, ValueError, json.JSONDecodeError):
        raise AgentError("Gateway unavailable or returned an invalid response.") from None

@dataclass
class AgentStep:
    agent: str
    task: str
    output: str
    input_tokens: int
    output_tokens: int
    estimated_usd: float | None
    generation_id: str | None
    duration_ms: int

def _chat(agent: str, policy: str, prompt: str, max_tokens: int) -> AgentStep:
    started = time.monotonic()
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": policy},
            {"role": "user", "content": prompt[:9000]}
        ],
        "temperature": 0.2, "max_tokens": max_tokens
    }
    response = _request("/chat/completions", payload)
    choices = response.get("choices") or []
    message = (choices[0].get("message") or {}) if choices else {}
    content = message.get("content")
    if isinstance(content, list):
        content = " ".join(c.get("text", "") for c in content if isinstance(c, dict))
    if not isinstance(content, str) or not content.strip():
        raise AgentError(agent + " returned no textual output.")
    usage = response.get("usage") or {}
    inp = usage.get("prompt_tokens")
    out = usage.get("completion_tokens")
    verified = isinstance(inp, int) and isinstance(out, int)
    # Unknown usage must never be represented as an actual provider token count.
    estimate = round((inp * INPUT_PRICE + out * OUTPUT_PRICE), 8) if verified else None
    return AgentStep(
        agent=agent, task=policy.split(".")[0][:110], output=content[:5000],
        input_tokens=inp if verified else -1,
        output_tokens=out if verified else -1,
        estimated_usd=estimate,
        generation_id=response.get("id") if isinstance(response.get("id"), str) else None,
        duration_ms=round((time.monotonic() - started) * 1000)
    )

def _source_digest(papers: list[dict]) -> str:
    return json.dumps([
        {"title":p["title"][:210], "doi":p["doi"],"doi_url":p["doi_url"],
         "year":p["year"], "publisher":p.get("publisher"),
         "title_relevance":p["title_relevance"]}
        for p in papers[:5]
    ], ensure_ascii=False)[:5800]

def orchestrate(topic: str) -> dict:
    """Source -> Analyst LLM -> Critic LLM -> Report LLM. No write tools."""
    if not configured():
        raise AgentError("LLM agents disabled. Set AI_AGENT_ENABLED=1, AGENT_ACCESS_TOKEN and Vercel OIDC/Gateway authentication.")
    if not isinstance(topic, str) or not 3 <= len(topic.strip()) <= 120:
        raise ValueError("Research topic must be between 3 and 120 characters.")
    topic = topic.strip()
    # Source Agent: actual Crossref live request; cannot be replaced by an LLM fabrication.
    papers = discover(topic, 5)
    if not papers:
        return {"project":"ResearchGuard","topic":topic,"sources":[],"stages":[],
                "report":"No source-backed publication metadata was found.",
                "billing":{"model":MODEL,"requests":0,"estimated_usd":0,
                           "actual_provider_invoice":"Not an invoice"}}
    sources = _source_digest(papers)
    steps = []
    # The three specialist prompts are independent LLM calls, not class labels.
    agents = [
        ("Analysis Agent",
         "You are a cautious bibliographic analysis specialist. Explain only what titles, publishers and years show. Never invent paper conclusions or methods.",
         "Topic: "+topic+"\nVerified source metadata (not full-text):\n"+sources+
         "\nWrite a short research landscape summary (max 130 words). Cite only DOI URLs provided."),
        ("Verification Agent",
         "You are an independent skeptical research auditor. Check the prior analysis against the provided metadata; identify overclaims, missing evidence and DOI references.",
         ""), # filled after analyst
        ("Report Agent",
         "You are an evidence-report editor. Produce a compact grounded report and limitations without unsupported scientific claims. Cite only the given DOI URLs.",
         "") # filled after auditor
    ]
    used = 0.0
    for i, (agent, policy, prompt) in enumerate(agents):
        if i == 1:
            prompt = "Topic: "+topic+"\nMetadata:\n"+sources+"\nAnalyst output:\n"+steps[0].output[:3200]+
                     "\nAudit this output. List unsupported inferences and safe corrections (max 110 words)."
        elif i == 2:
            prompt = "Topic: "+topic+"\nMetadata:\n"+sources+"\nAnalyst:\n"+steps[0].output[:2200]+
                     "\nIndependent audit:\n"+steps[1].output[:1800]+
                     "\nWrite final clear evidence memo with cited DOIs and caveats (max 180 words)."
        # Worst-case token reserve check; estimate includes capped output and capped prompt.
        cap = (len(prompt)//3 + 300) * INPUT_PRICE + 360*OUTPUT_PRICE
        if used + cap > MAX_RUN_ESTIMATE_USD:
            raise AgentError("Per-run estimated spending guardrail reached; no further AI calls.")
        step = _chat(agent, policy, prompt, max_tokens=360)
        steps.append(step)
        if step.estimated_usd is not None:
            used += step.estimated_usd
        else:
            # If the gateway omits token usage, stop; unknown bill must not be shown as $0.
            raise AgentError("Gateway omitted token usage; budget accounting is unavailable.")
    return {
        "project":"ResearchGuard", "mode":"llm-multi-agent", "topic":topic,
        "sources":papers, "stages":[asdict(step) for step in steps],
        "report":steps[-1].output,
        "billing":{
            "provider":"Vercel AI Gateway", "model":MODEL,
            "requests":len(steps),
            "input_tokens":sum(s.input_tokens for s in steps),
            "output_tokens":sum(s.output_tokens for s in steps),
            "estimated_usd":round(sum(s.estimated_usd for s in steps),8),
            "max_run_estimated_usd":MAX_RUN_ESTIMATE_USD,
            "pricing_as_of":"2026-11-24",
            "actual_provider_invoice":"Not an invoice; check your Vercel AI Gateway Billing and Logs."
        },
        "limitations":[
            "Crossref metadata proves neither article conclusions nor research claim correctness.",
            "AI agent analysis can be inaccurate; verify original papers.",
            "The USD amount is a model-price estimate, not actual Vercel-billed spend.",
            "No paid request is made unless the operator authenticates and activates agents."
        ]
    }

def credit_balance():
    """Official balance from Vercel AI Gateway; no model generation and no local estimates."""
    if not configured():
        raise AgentError("AI Gateway operator mode is not enabled.")
    obj = _request("/credits")
    # Do not invent keys; return only non-secret billing aggregate fields.
    return {k:v for k,v in obj.items() if k in {
        "balance","total_used","total_spent","currency","credits","lifetime_usage",
        "remaining","remaining_balance","spend","paid_credits","free_credits"}}
