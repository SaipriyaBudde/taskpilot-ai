from app.core.llm_client import generate
from app.core.prompts import VISUAL_PROMPT


class VisualAgent:
    def run(self, tasks: list[dict], summary: str | None = None) -> str | None:
        if not tasks and not summary:
            return None

        task_list = "\n".join(f"- {task['task']}" for task in tasks if "task" in task)

        prompt = VISUAL_PROMPT.format(
            tasks=task_list,
            summary=summary or "No summary available."
        )

        output = generate(prompt).strip()
        return output if output else None