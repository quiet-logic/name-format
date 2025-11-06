from __future__ import annotations
import re

# Particles that usually stay lowercase when not the first token
LOWER_PARTICLES = {
    "de", "da", "del", "della", "der", "den",
    "van", "von", "vom", "zu", "zur",
    "di", "du", "des",
    "la", "le",
    "of", "the",
}

INITIAL_RE = re.compile(r"^[A-Za-z]\.?$")

def _is_initial(tok: str) -> bool:
    return bool(INITIAL_RE.match(tok))

def _format_initial(tok: str) -> str:
    # "a" or "a." -> "A."
    return tok[0].upper() + "."

def _smart_cap_core(word: str) -> str:
    """Title-case a token but preserve inner apostrophes/hyphens."""
    def cap_piece(p: str) -> str:
        return p[:1].upper() + p[1:].lower() if p else p

    # handle apostrophes, then hyphens per segment
    apos_parts = word.split("'")
    apos_parts = ["-".join(cap_piece(h) for h in p.split("-")) for p in apos_parts]
    return "'".join(apos_parts)

def _smart_cap(word: str) -> str:
    """Mc/Mac + title-casing with inner punctuation preserved."""
    w = word
    lw = w.lower()

    # Mc / Mac handling
    if lw.startswith("mc") and len(w) > 2:
        return "Mc" + w[2:3].upper() + w[3:].lower()
    if lw.startswith("mac") and len(w) > 3:
        return "Mac" + w[3:4].upper() + w[4:].lower()

    return _smart_cap_core(w)

def _normalise_quotes(s: str) -> str:
    # normalise curly quotes to straight apostrophes
    return s.replace("’", "'").replace("‘", "'")

def _tokens_from_input(*parts: str) -> list[str]:
    # join all parts, normalise quotes, turn separator punct into spaces, split
    s = " ".join(parts)
    s = _normalise_quotes(s).strip()
    s = re.sub(r"[,\.;:/|]+", " ", s)
    tokens = s.split()
    return tokens

def _format_token(tok: str, position: int) -> str:
    t = tok.strip()
    if not t:
        return t

    if _is_initial(t):
        return _format_initial(t)

    # lowercase particles when not first
    if position > 0 and t.lower() in LOWER_PARTICLES:
        return t.lower()

    return _smart_cap(t)

def _normalise_attached_irish_o(tok: str) -> str:
    """Turn óxxxx / oxxxx (no apostrophe) into O'Xxxx."""
    if not tok:
        return tok
    t = tok.lower()
    # already has apostrophe like o'brien? leave to _smart_cap_core
    if "'" in tok:
        return _smart_cap(tok)

    # attached óxxxx or oxxxx (letters only) -> O'Xxxx
    if t[0] in {"o", "ó"} and len(tok) > 1 and t[1:].isalpha():
        return "O'" + _smart_cap_core(tok[1:])
    return _smart_cap(tok)

def full_name(*name_parts: str) -> str:
    """
    Accepts:
      - full_name("first last")
      - full_name("first", "last")
      - full_name("ó brian")            -> O'Brian
      - full_name("óbrien")             -> O'Brien
      - full_name("michael patrick o'sullivan") -> Michael O'Sullivan
    Rules:
      - Normalises curly quotes.
      - Keeps initials (A. B. etc).
      - Keeps particles like 'de', 'van' when not first.
      - Hyphens and apostrophes preserved.
      - Mc/Mac handled.
    """
    tokens = _tokens_from_input(*name_parts)
    if not tokens:
        raise ValueError("No name parts found.")

    # Single token cases (e.g., "óbrien", "prince")
    if len(tokens) == 1:
        tok = tokens[0]
        if _is_initial(tok):
            return _format_initial(tok)
        # handle attached Irish O/Ó
        return _normalise_attached_irish_o(tok)

    # Two-token special case: "ó brian" / "o brian" -> O'Brian (surname only)
    if len(tokens) == 2 and tokens[0].lower() in {"o", "ó"} and tokens[1].isalpha():
        return "O'" + _smart_cap_core(tokens[1])

    # General case: treat as full name → first + last (with particle-aware last)
    # First name:
    first_token = tokens[0]
    first = _format_token(first_token, position=0)

    # Determine last name; keep preceding particle if present (e.g., "de Valera")
    if len(tokens) >= 3 and tokens[-2].lower() in LOWER_PARTICLES:
        last = _format_token(tokens[-2], position=len(tokens) - 2) + " " + _smart_cap(tokens[-1])
    else:
        # also normalise attached Ó/ O cases on last token
        last = _normalise_attached_irish_o(tokens[-1])

    return f"{first} {last}"