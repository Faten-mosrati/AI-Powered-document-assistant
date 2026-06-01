import asyncio
from collections import Counter
from app.models.schemas import Email, TriageItem, AgentRunResponse
from app.services.classifier import classify_email
from app.services.drafter import draft_reply


async def _process_one(email: Email) -> TriageItem:
    """Per-email pipeline: classify, then draft only if a reply is needed.

    Sequential within an email because the draft decision depends on the classification:
    if needs_reply is false (newsletter, FYI, spam), we skip the draft call entirely
    and save the tokens. Parallelizing classify+draft speculatively would waste tokens
    on every newsletter."""
    classification = await classify_email(email)
    draft = None
    if classification.needs_reply:
        draft = await draft_reply(email)
    return TriageItem(email=email, classification=classification, draft=draft)


async def run_agent(emails: list[Email]) -> AgentRunResponse:
    """Process a batch of emails concurrently.

    asyncio.gather fans out — all emails are processed in parallel. For a 20-email
    inbox this turns a 60-second sequential run into ~5 seconds concurrent.

    Caveat: Azure has per-deployment rate limits (RPM and TPM). For large batches,
    wrap this in asyncio.Semaphore(N) to cap concurrency. For batches under ~20 on a
    standard deployment, this is fine as-is."""
    items = await asyncio.gather(*[_process_one(e) for e in emails])
    summary = dict(Counter(item.classification.category.value for item in items))
    return AgentRunResponse(items=items, summary=summary)
