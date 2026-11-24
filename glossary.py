"""Free Dictionary API enrichment for academic English terminology.

Read-only FastMCP research glossary utility. Dictionary definitions are not
sources for factual scientific claims or citation verification.
"""
from __future__ import annotations
import re
from urllib.parse import quote
from transport import request_json, SourceError

def define_term(word: str) -> dict:
    if not isinstance(word, str) or not re.fullmatch(r"[A-Za-z][A-Za-z '-]{0,49}", word.strip()):
        raise ValueError("Use one English word or short hyphenated term (1–50 characters).")
    term = word.strip().lower()
    data = request_json("https://api.dictionaryapi.dev/api/v2/entries/en/" + quote(term, safe=""))
    if not isinstance(data, list):
        raise SourceError("Dictionary API did not return a word entry.")
    senses=[]
    for e in data[:2]:
        for meaning in (e.get("meanings") or [])[:3]:
            for definition in (meaning.get("definitions") or [])[:2]:
                d=definition.get("definition")
                if isinstance(d,str) and d:
                    senses.append({"part_of_speech":meaning.get("partOfSpeech"),
                                   "definition":d[:500]})
    return {
        "word":term, "definitions":senses[:6],
        "source_url":"https://dictionaryapi.dev/",
        "provider":"Free Dictionary API",
        "limitations":["Dictionary meanings are not scientific citations or evidence of research conclusions."]
    }
