from app.models.schemas import Email, DraftResult
from app.prompts.draft import DRAFT_SYSTEM_PROMPT, build_draft_user_prompt
from app.services.azure_client import get_client
from app.config import settings


async def draft_reply(email: Email) -> DraftResult:
    """Drafts a reply using Azure OpenAI structured outputs.

    Uses .parse() so the response is guaranteed to match the DraftResult schema.
    No manual JSON parsing.

    Temperature 0.4 — drafting should sound natural, not deterministic.
    """
    client = get_client()
    response = await client.beta.chat.completions.parse(
        model=settings.azure_openai_chat_deployment,
        messages=[
            {"role": "system", "content": DRAFT_SYSTEM_PROMPT},
            {"role": "user", "content": build_draft_user_prompt(email)},
        ],
        response_format=DraftResult,
        temperature=0.4,
    )
    return response.choices[0].message.parsed