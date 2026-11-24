"""ResearchGuard: auditable Crossref discovery -> metadata verification -> report."""
from __future__ import annotations
import os
import re
from difflib import SequenceMatcher
from urllib.parse import quote
from transport import request_json, SourceError

SERVICES = ["ResearchGuard"]
DOI = re.compile(r"^10\.\d{4,9}/\S{1,200}$", re.I)

def _clean(value):
    return " ".join(re.sub(r"[^a-z0-9]+", " ", str(value).lower()).split())

def _score(query: str, title: str) -> float:
    q, t = _clean(query), _clean(title)
    return round(SequenceMatcher(None, q, t).ratio(), 3) if q and t else 0.0

def _paper(item):
    title = next(iter(item.get("title") or []), "")
    doi = item.get("DOI", "")
    if not title or not doi or not DOI.fullmatch(doi):
        return None
    date = item.get("published", {}).get("date-parts") or [[None]]
    return {
        "title": title,
        "doi": doi,
        "doi_url": "https://doi.org/" + quote(doi, safe="/"),
        "publisher": item.get("publisher"),
        "year": date[0][0] if date and date[0] else None,
        "authors": [
            " ".join(filter(None, [a.get("given"), a.get("family")]))
            for a in (item.get("author") or [])[:5]
        ],
        "metadata_source": "Crossref"
    }

def discover(topic: str, limit: int = 6):
    if not isinstance(topic, str) or not 2 <= len(topic.strip()) <= 120:
        raise ValueError("Topic must be 2–120 characters.")
    limit = min(max(1, int(limit)), 10)
    # Source Agent: official public metadata, not an LLM-generated reference.
    data = request_json("https://api.crossref.org/works",
                        {"query.bibliographic": topic.strip(), "rows": min(limit*3, 30),
                         "select": "DOI,title,publisher,published,author"})
    items = data.get("message", {}).get("items", [])
    if not isinstance(items, list):
        raise SourceError("Crossref returned unexpected data.")
    # Analysis Agent: normalized, deduplicated and deterministically ranked.
    seen, papers = set(), []
    for item in items:
        paper = _paper(item)
        if not paper or paper["doi"].lower() in seen:
            continue
        seen.add(paper["doi"].lower())
        paper["title_relevance"] = _score(topic, paper["title"])
        papers.append(paper)
    return sorted(papers, key=lambda p: p["title_relevance"], reverse=True)[:limit]

def verify_doi(doi: str):
    """Verify existence of DOI metadata, NOT support for claims in the paper."""
    if not isinstance(doi, str) or not DOI.fullmatch(doi.strip()):
        raise ValueError("Please provide a valid DOI, e.g. 10.1038/415026a.")
    doi = doi.strip()
    item = request_json("https://api.crossref.org/works/" + quote(doi, safe=""))
    paper = _paper(item.get("message", {}))
    if paper is None:
        return {"metadata_verified": False, "doi": doi, "reason": "DOI record had missing fields"}
    paper["metadata_verified"] = paper["doi"].lower() == doi.lower()
    return paper

def report(topic: str, limit: int = 6):
    if DOI.fullmatch(topic.strip()):
        return {"project": "ResearchGuard", "mode": "verify_doi",
                "result": verify_doi(topic), "source": "https://api.crossref.org",
                "limitations": ["DOI metadata verification does not verify full-text claims."]}
    papers = discover(topic, limit)
    # Verification Agent: references must be source-linked; relevance is not truth.
    verified = [p for p in papers if p["doi_url"].startswith("https://doi.org/")]
    # Report Agent: include original links, unsupported claim warnings and source coverage.
    return {
        "project": "ResearchGuard", "query": topic, "stages": [
            "SourceAgent: Crossref metadata",
            "AnalysisAgent: DOI deduplication and title similarity",
            "VerificationAgent: DOI format and source links",
            "ReportAgent: transparent evidence shortlist",
        ],
        "paper_count": len(verified), "papers": verified,
        "source": "https://api.crossref.org/works",
        "optional_openalex": "Set OPENALEX_API_KEY to enable a future OpenAlex cross-check; not used in this release.",
        "limitations": [
            "Title relevance is not scientific evidence for any specific claim.",
            "Crossref records are publisher-contributed metadata and may be incomplete.",
            "Read original studies, methods and results before citing conclusions.",
            "No autonomous literature review or LLM reasoning is performed."
        ]
    }

def run(query: str, service: str = "ResearchGuard"):
    if service not in SERVICES:
        raise ValueError("Unknown service.")
    return report(query)

if __name__ == "__main__":
    import argparse, json
    ap = argparse.ArgumentParser(description="ResearchGuard source-grounded paper discovery")
    ap.add_argument("query", help="Topic or DOI")
    ap.add_argument("--limit", type=int, default=6)
    args = ap.parse_args()
    try:
        print(json.dumps(report(args.query, args.limit), indent=2))
    except (SourceError, ValueError) as exc:
        ap.exit(2, "ResearchGuard: " + str(exc) + "\n")
