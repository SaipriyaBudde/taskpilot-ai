import json

from app.core.llm_client import extract_json_block, generate
from app.core.prompts import PRESENTATION_PROMPT


class PresentationAgent:
    def run(self, tasks: list[dict], summary: str | None = None) -> list[dict]:
        if not tasks and not summary:
            return []

        payload = {
            "tasks": tasks,
            "summary": summary,
        }

        prompt = PRESENTATION_PROMPT.format(context=json.dumps(payload, indent=2))
        output = generate(prompt)
        cleaned_output = extract_json_block(output)

        try:
            slides = json.loads(cleaned_output)

            if not isinstance(slides, list):
                return []

            valid_slides = []
            for item in slides:
                if not isinstance(item, dict):
                    continue

                bullets = item.get("bullets", [])
                if not isinstance(bullets, list):
                    bullets = []

                valid_slides.append(
                    {
                        "title": item.get("title", "Untitled Slide"),
                        "bullets": [str(bullet) for bullet in bullets],
                    }
                )

            return valid_slides

        except json.JSONDecodeError:
            return []