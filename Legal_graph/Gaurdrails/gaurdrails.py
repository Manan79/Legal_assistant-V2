from Legal_graph.Gaurdrails.colang_rules import COLANG_CONTENT,YAML_CONTENT
import re
from typing import Optional
from nemoguardrails import RailsConfig, LLMRails
from nemoguardrails.actions import action
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

# ── Detection helpers ─────────────────────────────────────────────────────────

BLOCK_RE   = re.compile(r'\[RAIL_BLOCKED(?::(\w+))?\]')


BLOCK_LABELS = {
    "OFF_TOPIC":    "Off-topic question",
    "JAILBREAK":    "Jailbreak attempt",
    "CONFIDENTIAL": "Confidential employee data",
    "PII":          "PII detected in input",
}


def parse_nemo_response(raw):
    """
    Normalise NeMo response (dict or str) to a plain string.
    Returns (text, is_blocked, block_reason, is_dialog, needs_rag).
    """
    if isinstance(raw, dict):
        text = raw.get("content") or raw.get("text") or raw.get("message") or str(raw)
    elif raw is None:
        text = ""
    else:
        text = str(raw)

    block_match = BLOCK_RE.search(text)
    if block_match:
        reason = block_match.group(1)
        clean  = BLOCK_RE.sub("", text).strip()
        return clean, True, reason, False, False



@action(is_system_action=True)
async def detect_pii(context: Optional[dict] = None):
    """Returns list of PII type names found, or empty list if clean."""
    msg = context.get("user_message", "") if context else ""
    patterns = {
        "email":       r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "phone":       r"\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b",
        "ssn":         r"\b\d{3}-\d{2}-\d{4}\b",
        "api_key":     r"(api[_\s-]?key|token|secret)[:\s]+[A-Za-z0-9_\-]{10,}",
        "credit_card": r"\b\d{4}[\s-]\d{4}[\s-]\d{4}[\s-]\d{4}\b",
    }
    return [name for name, pat in patterns.items() if re.search(pat, msg, re.IGNORECASE)]


# ── Build rails ───────────────────────────────────────────────────────────────

def build_rails(llm) -> LLMRails:
    config = RailsConfig.from_content(
        colang_content=COLANG_CONTENT,
        yaml_content=YAML_CONTENT,
    )
    rails = LLMRails(config, llm=llm)
    rails.register_action(detect_pii)
    return rails


llm   = ChatGroq(model='openai/gpt-oss-120b', temperature=0)
rails = build_rails(llm)

