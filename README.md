# ResearchGuard · Research metadata verifier

A source-grounded, **working Python prototype** for academic citation discovery and DOI bibliographic checks. Crossref metadata is retrieved live when you run a query. It **cannot verify scientific claims** or replace reading the papers.

### Agents and tools
SourceAgent (Crossref) → AnalysisAgent (title similarity and DOI deduplication) → VerificationAgent (DOI format and source links) → ReportAgent (JSON evidence shortlist) → human review.

**API:** [Crossref REST](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) (public). OpenAlex is a future enhancement: its free API key, when required, belongs in environment variables, never the repository.

### Run
Python 3.11+:
```bash
python core.py "machine learning for education"
python core.py "10.1038/415026a"
python dashboard.py --port 8765
python -m unittest discover -s tests -v
```
Open http://localhost:8765 for the dark browser dashboard.

Optional MCP client: `pip install -r requirements.txt`, then `python server.py` (stdio) or `fastmcp run server.py:mcp --transport http --port 8000`. Requires a compatible MCP client; HTTP MCP must be secured before publishing.

### Status and boundaries
- Source: public Crossref metadata, accessed on request
- No API key needed for the default query
- Three read-only FastMCP tools
- Tests use mocked records, not fictitious live data
- Production LLM agent, OpenAlex cross-check and full-text claim checking: **not implemented**
- Transport may return HTTP/timeouts on rate limits; errors are surfaced, not hidden

The browser dashboard is local by default. This repository is not an automatically deployed SaaS.
