"""FastMCP tool interface for ResearchGuard. Install: pip install -r requirements.txt."""
from fastmcp import FastMCP
from core import report, verify_doi, discover
from glossary import define_term

mcp = FastMCP("MUHRIS ResearchGuard")

@mcp.tool
def find_research(topic: str, limit: int = 6) -> dict:
    """Discover real publications with Crossref DOI metadata and source URLs."""
    return report(topic, limit)

@mcp.tool
def inspect_doi(doi: str) -> dict:
    """Confirm DOI bibliographic metadata; NOT scientific claims."""
    return verify_doi(doi)

@mcp.tool
def find_papers(topic: str, limit: int = 6) -> list[dict]:
    """Retrieve raw evidence-linked citation candidates from Crossref."""
    return discover(topic, limit)

@mcp.tool
def explain_english_term(word: str) -> dict:
    """Retrieve source-linked English definitions; not scientific fact-checking."""
    return define_term(word)

if __name__ == "__main__":
    mcp.run()
