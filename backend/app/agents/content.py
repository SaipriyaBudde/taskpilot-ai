from app.core.llm_client import generate
from app.core.prompts import CONTENT_SUMMARY_PROMPT


class ContentAgent:
    def run(self, user_input: str) -> str | None:
        prompt = CONTENT_SUMMARY_PROMPT.format(user_input=user_input)
        output = generate(prompt).strip()

        return output if output else None