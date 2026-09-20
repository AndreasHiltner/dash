"""Deterministic knowledge-base search for the /dash helpdesk."""

import re
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"

# Common DE/EN function words. They carry no topical signal and their
# substrings pollute scoring (query "was soll das tun?" — "das" matched
# "dash" and surfaced the irrelevant Core Commands section).
STOP_WORDS = {
    # German
    "das", "die", "der", "den", "dem", "des", "und", "oder", "aber", "was",
    "wie", "wer", "wen", "wem", "warum", "wieso", "wo", "wann", "soll",
    "sollst", "sollte", "tun", "macht", "machen", "ist", "sind", "sein",
    "war", "ein", "eine", "einen", "einer", "einem", "eines", "mit", "für",
    "auf", "aus", "bei", "von", "zu", "im", "in", "an", "nicht", "kein",
    "keine", "bitte", "mir", "mich", "dir", "dich", "ich", "du", "es",
    "sie", "er", "wir", "ihr", "man", "hat", "habe", "haben", "kann",
    "kannst", "könnte", "will", "willst", "würde", "geht", "funktioniert",
    "heißt", "bedeutet", "genau", "einfach", "mal", "kurz", "frage",
    # English
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "do",
    "does", "did", "what", "how", "why", "when", "where", "which", "who",
    "can", "could", "should", "would", "will", "to", "of", "in", "on",
    "at", "for", "with", "it", "this", "that", "my", "me", "you", "i",
    "and", "or", "but", "not", "no", "please", "just", "about",
}

# High-frequency domain words. A single one of these matching only a body is
# NOT a discriminative signal — "desktop", "tab", "session", "plugin" appear
# in almost every section, so a lone body hit would surface the wrong answer.
GENERIC_TERMS = {
    "plugin", "plugins", "session", "sessions", "desktop", "tab", "tabs",
    "hermes", "gateway", "command", "commands", "pane", "panes", "dash",
    "agent", "agents", "window", "windows", "bot", "bots",
}


def _sections(text: str) -> list[str]:
    """Splits into '## Section' chunks, dropping the H1 preamble.

    The file title line ('# Hermes Core Knowledge') is metadata, not an answer
    — searching it yields header-only hits like '# Hermes Desktop Knowledge'.
    """
    parts = text.split("\n## ")
    # parts[0] = H1 preamble; everything after starts with the section name.
    return parts[1:]


def _terms(query: str) -> list[str]:
    """Lowercased, stop-word-free query terms (>2 chars)."""
    return [
        t.lower()
        for t in query.split()
        if len(t) > 2 and t.lower() not in STOP_WORDS
    ]


def _heading_and_body(section: str) -> tuple[str, str]:
    """A section is '<heading>\n<body>'; split on the first newline.

    Heading matches weight more than body matches: a section NAMED 'Plugins'
    is a stronger signal than a passing mention of 'plugins' in some body.
    """
    heading, _, body = section.partition("\n")
    return heading, body


def _matched(text_lower: str, terms: list[str]) -> set[str]:
    """Word-boundary term hits. Substring matching is a false-positive
    machine: 'das' ⊂ 'dash', 'api' ⊂ 'escaping'. Boundaries require the term
    to stand as its own token (or exact literal like 'ctrl+shift+p')."""
    return {
        t for t in terms
        if re.search(rf"\b{re.escape(t)}\b", text_lower)
    }


def search(query: str) -> str | None:
    """Returns the most relevant '## section' as text, or None.

    Ranking: heading hits first, then body hits. A single generic domain
    word matching only a body is discarded — it can't distinguish one section
    from another, so the LLM fallback gets the question instead.
    """
    terms = _terms(query)
    if not terms:
        return None
    best, best_h, best_b = None, -1, -1
    best_body_matched: set[str] = set()
    for md in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        for section in _sections(text):
            heading, body = _heading_and_body(section)
            h_matched = _matched(heading.lower(), terms)
            b_matched = _matched(body.lower(), terms)
            key = (len(h_matched), len(b_matched))
            if key > (best_h, best_b):
                best_h, best_b = key
                best = section
                best_body_matched = b_matched
    if best is None or best_h + best_b == 0:
        return None
    # Lone generic body hit → no real signal → fall through to the LLM.
    if best_h == 0 and best_b == 1 and next(iter(best_body_matched)) in GENERIC_TERMS:
        return None
    # Restore the '## ' prefix so the answer renders as a heading + body.
    return f"## {best}"
