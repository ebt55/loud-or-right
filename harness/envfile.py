"""Minimal .env reader. Standard library only.

load(path=None) -> dict of NAME -> value. Lines are NAME=value; blank lines and lines starting with '#'
are skipped; a trailing ' #...' comment after a value is NOT stripped (values have no quotes and may
contain '#'). Surrounding whitespace is trimmed. Nothing is written to os.environ, nothing is printed.
Values are secrets: callers must never print or log them (use secret_values() to scrub text).
"""
import os

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")

# Names whose values are credentials (scrubbed from any error text). Budgets and locations are not secret.
SECRET_NAMES = ("OPENAI_API_KEY", "OPENAI_ORG_ID", "OPENAI_PROJECT_ID", "GEMINI_API_KEY",
                "ANTHROPIC_API_KEY", "OPENROUTER_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS",
                "GOOGLE_CLOUD_PROJECT")


def load(path=None):
    """Parse the file into a dict. A missing file gives {}. Malformed lines are skipped silently
    (never echoed, since they may hold a key)."""
    path = path or DEFAULT_PATH
    out = {}
    try:
        with open(path, encoding="utf-8-sig") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return out
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        name, value = s.split("=", 1)
        name = name.strip()
        if name.startswith("export "):
            name = name[len("export "):].strip()
        if not name or not name.replace("_", "").isalnum():
            continue
        out[name] = value.strip()
    return out


def secret_values(env):
    """The non-empty credential values in env, longest first (for scrubbing)."""
    vals = {v for k, v in env.items() if k in SECRET_NAMES and v and len(v) >= 4}
    return sorted(vals, key=len, reverse=True)


def scrub(text, env):
    """Replace every credential value from env that occurs in text with '[REDACTED]'."""
    if not text:
        return text
    for v in secret_values(env):
        text = text.replace(v, "[REDACTED]")
    return text
