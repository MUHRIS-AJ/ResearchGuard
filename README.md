# ResearchGuard — real multi-agent research studio

**Current release candidate: v0.2 / source-grounded multi-agent AI.**

A browser-based academic literature discovery and research-assistance application. It retrieves real Crossref publication metadata, runs three distinct LLM stages when explicitly enabled and authorized, and reports **provider-reported input/output tokens** with a model-price estimate. Its FastMCP server exposes separate read-only research and glossary tools.

> **Important:** Model-backed mode is disabled unless the owner configures a provider key and operator token. The public source-search mode works without an LLM key. There is no automatic API subscription, stored payment card, fabricated invoice, or always-on agent swarm.

## Try the public dashboard

**[ResearchGuard on Vercel](https://muhris-researchguard.vercel.app/)**

- Public: discover real Crossref publication metadata without paid model calls
- Private (operator only): three separate LLM requests for analysis, independent skeptical audit and report writing
- Live usage: token counts from each provider response (not guesses)
- Estimated API cost: published unit rates times actual tokens, per agent and current browser session
- Official billing: Vercel AI Gateway account / Groq Console
- Crossref DOI links retained in the final report, with limitations

## Actual architecture

```text
User / authenticated operator
          |
    ResearchGuard API
          |
  Source Agent (Crossref)
          |
  Citation metadata evidence set
          |
   Analysis LLM Agent -------- 1 model request
          |
 Verification/Audit LLM ------ 1 model request
          |
     Report LLM Agent -------- 1 model request
          |
   Auditable report + DOI links + per-agent token usage and price estimate
          |
       Human review
```

These agents are **separate model invocations**, orchestrated in a bounded and serial execution graph. They are not a continuously autonomous workforce: no external accounts are modified and no background tasks are executed. The Verification Agent checks overstatements against bibliographic metadata, **not scientific claim truth or full text**.

### Data, frameworks and MCP tools

- **Crossref:** https://api.crossref.org/works; real publication metadata, no default API key
- **Free Dictionary API:** https://api.dictionaryapi.dev; academic English glossary, not scientific evidence
- **FastMCP:** separate read-only `find_research`, `inspect_doi`, `find_papers`, and `explain_english_term` tools
- **FastAPI:** server-side API and polished responsive browser control room
- **Model provider A:** Vercel AI Gateway, model `google/gemini-2.5-flash-lite`
- **Model provider B:** **official Groq API**, model `openai/gpt-oss-20b` (free plan **subject to eligibility and rate limits**; never assume free)
- All source URLs and model hosts are fixed by server code, never supplied by the public user.

## Setup (Python 3.11+)

```bash
python -m venv .venv
# Activate your environment, then:
pip install -r requirements.txt
python -m unittest discover -s tests -v
python core.py "AI in education"
python dashboard.py --port 8765  # Old local source-only viewer
uvicorn app:app --host 127.0.0.1 --port 8000 # New dashboard
```

Open http://127.0.0.1:8000 for the full research console. **AI access remains disabled without environment configuration.**

### Enable Groq official free-tier-compatible LLM calls

Use provider-issued credentials in your hosting settings or a private, uncommitted environment. Do not paste keys into GitHub, ChatGPT, or a public issue:

```dotenv
AI_LLM_PROVIDER=groq
GROQ_API_KEY=<set privately in your host>
AGENT_ACCESS_TOKEN=<owner-generated long random secret; at least 24 characters>
AI_AGENT_ENABLED=1
```

The operator enters only the `AGENT_ACCESS_TOKEN` into the console. The real Groq key stays server-side. If Groq free usage is exhausted or your account requires billing, the provider returns an error; the application does not attempt to bypass quotas. **Use Groq's official dashboard for actual usage and charges.**

### Enable Vercel AI Gateway instead

```dotenv
AI_LLM_PROVIDER=gateway
AI_GATEWAY_API_KEY=<set privately; alternatively use platform-provided VERCEL_OIDC_TOKEN>
AGENT_ACCESS_TOKEN=<owner-generated long random secret; at least 24 characters>
AI_AGENT_ENABLED=1
```

Vercel's AI Gateway may require billing verification, credits, and suitable spend limits before model requests work. We do **not** enable payments or create provider keys for the user. Configure a provider-level budget before turning on paid mode.

### Billing accuracy and safety

| Metric | Dashboard meaning |
|---|---|
| Input/output tokens | As returned by each successful model API response |
| Per-stage price | Reference USD/token on **2026-11-24** (not live price sync) |
| Session estimate | Sum of estimated prices for steps completed in that page session |
| $0.01 software guard | Estimated per-workflow limit (not a durable account budget) |
| Official invoice / charges | **Only** from the selected provider's billing dashboard |
| API model keys | Never returned to the browser or committed |
| Source requests | Crossref public metadata; separate from model tokens |

Reference rates (USD per 1M tokens): Vercel Gemini 2.5 Flash Lite **$0.10 input / $0.40 output**; Groq GPT-OSS 20B **$0.075 input / $0.30 output**. Free plan, discounts, model deprecations and quota limits may change. The site makes no model requests unless authenticated operator mode is explicitly enabled.

No permanent usage database, generated tax invoice, team-wide spend limits, payment processing, user accounts, or multi-tenant support is claimed. Use Vercel AI Gateway budgets / Groq account spending limits for enforceable provider-side caps. Treat the operator secret like a password.

### MCP access

```bash
python server.py
```

The default is local stdio, suitable for explicitly configured MCP clients. Don't expose unauthenticated FastMCP tools to the public internet. For registry and security guidance consult https://modelcontextprotocol.io/ and https://github.com/modelcontextprotocol/servers; reference examples are **not automatically production hardened**.

### Verification

```bash
python -m compileall -q .
python -m unittest discover -s tests -v
```

Tests mock source/provider responses to verify orchestration, price arithmetic and failure behavior. They are **not** proof that an actual account can call the selected model. To complete genuine LLM live testing, the repository owner must configure a legitimate provider account/key and private operator token.

**[Reviewed external GitHub API/MCP resources](docs/EXTERNAL_SOURCES.md)**

## Privacy, trust and non-goals

- The system only sends the user's research topic and a bounded, source-linked metadata shortlist to the configured LLM provider.
- A reference to a DOI is not validation of a paper's conclusions.
- No access to personal Gmail, documents, or private files is needed.
- No API credentials are shipped in the browser. No free proxy or quota circumvention is built in.
- No physical hazard or safety warning features.
