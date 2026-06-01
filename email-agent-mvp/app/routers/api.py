"""All HTTP endpoints in one place.

Kept together because the API surface is small (4 endpoints). When it grows past
~8 endpoints or develops clear sub-domains (e.g. /admin/*, /feedback/*), split
into multiple routers. Premature splitting just adds files to navigate.

Each handler is intentionally thin: parse the request, call a service, return.
No business logic here — that lives in app/services/.
"""

from fastapi import APIRouter

from app.models.schemas import (
    AgentRunRequest,
    AgentRunResponse,
    ClassificationResult,
    ClassifyRequest,
    DraftRequest,
    DraftResult,
)
from app.services.agent import run_agent
from app.services.classifier import classify_email
from app.services.drafter import draft_reply

router = APIRouter()


@router.get("/health", tags=["meta"])
async def health():
    """Liveness probe. NestJS hits this to know the Python service is up."""
    return {"status": "ok"}


@router.post("/classify", response_model=ClassificationResult, tags=["agent"])
async def classify(req: ClassifyRequest):
    """Classify a single email. Useful for debugging the classifier in isolation,
    and for the eventual case where NestJS wants to classify on Gmail push (one
    email at a time) rather than batch."""
    return await classify_email(req.email)


@router.post("/draft", response_model=DraftResult, tags=["agent"])
async def draft(req: DraftRequest):
    """Generate a single reply draft. Called either directly (user clicks
    'regenerate' in the UI) or internally by the agent loop."""
    return await draft_reply(req.email)


@router.post("/agent/run", response_model=AgentRunResponse, tags=["agent"])
async def agent_run(req: AgentRunRequest):
    """The main entry point. NestJS sends a batch of fresh emails (fetched from
    Gmail via MCP) and gets back classified emails with drafts for the ones
    needing replies.

    The endpoint contract doesn't depend on how emails were obtained — NestJS
    owns the Gmail integration, this service only does LLM work."""
    return await run_agent(req.emails)
