from app.models.schemas import Email, ClassificationResult
from app.prompts.classify import CLASSIFY_SYSTEM_PROMPT, build_classify_user_prompt
from app.services.azure_client import get_client
from app.config import settings


async def classify_email(email: Email) -> ClassificationResult:
    """Calls Azure OpenAI with structured outputs to classify an email.

    Why .parse() instead of .create() + json.loads():
    - The model is constrained to produce JSON matching the ClassificationResult
      schema exactly. Out-of-enum categories, missing fields, wrong types — all
      become structurally impossible, not just validated after the fact.
    - The SDK returns a parsed Pydantic instance directly. No manual json.loads,
      no **data unpacking, no try/except around malformed JSON.
    - Structured outputs mode is more reliable than the older json_object mode.
      The model conforms to the schema, not just "some JSON".

    Temperature 0.1 because classification is a decision task — same input should
    always give the same category.
    """
    client = get_client()
    response = await client.beta.chat.completions.parse(
        model=settings.azure_openai_chat_deployment,
        messages=[
            {"role": "system", "content": CLASSIFY_SYSTEM_PROMPT},
            {"role": "user", "content": build_classify_user_prompt(email)},
        ],
        response_format=ClassificationResult,
        temperature=0.1,
    )
    return response.choices[0].message.parsed