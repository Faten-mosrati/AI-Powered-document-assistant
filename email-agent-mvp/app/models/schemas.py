from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class EmailCategory(str, Enum):
    URGENT = "urgent"
    WAITING_ON_ME = "waiting_on_me"
    FYI = "fyi"
    NEWSLETTER = "newsletter"
    QUIET_SPAM = "quiet_spam"


class Email(BaseModel):
    """Normalized email shape. This is what NestJS will feed us after fetching from
    Gmail via MCP. Keeping it stable means the rest of the code doesn't care where
    emails come from."""

    message_id: str
    thread_id: str
    from_address: str = Field(..., alias="from")  # "from" is a Python keyword
    to: list[str]
    subject: str
    body: str
    received_at: datetime
    thread_history: Optional[list[str]] = None  # prior message bodies, oldest first

    model_config = {"populate_by_name": True}


class ClassificationResult(BaseModel):
    """Result of classifying an email.

    Note: no Field(ge=0.0, le=1.0) constraints on confidence — OpenAI's structured
    outputs uses a restricted subset of JSON Schema that doesn't support numeric
    minimum/maximum. The prompt tells the model to keep confidence in [0, 1], and
    that's enough in practice.
    """
    category: EmailCategory
    confidence: float
    reasoning: str
    needs_reply: bool


class DraftResult(BaseModel):
    """Result of drafting a reply.

    Same note on confidence — no range constraint at the schema level.
    """
    draft: str
    language: str  # "en", "fr", etc — detected from the incoming email
    confidence: float
    notes: Optional[str] = None  # e.g., "lacked context, drafted conservatively"


# ---- Request / response shapes for endpoints ----

class ClassifyRequest(BaseModel):
    email: Email


class DraftRequest(BaseModel):
    email: Email


class AgentRunRequest(BaseModel):
    emails: list[Email]


class TriageItem(BaseModel):
    email: Email
    classification: ClassificationResult
    draft: Optional[DraftResult] = None


class AgentRunResponse(BaseModel):
    items: list[TriageItem]
    summary: dict[str, int]  # category -> count, for the daily digest