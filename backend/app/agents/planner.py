import json

from app.core.llm_client import extract_json_block, generate
from app.core.prompts import TASK_PLANNER_PROMPT


class TaskPlanner:
    def run(self, user_input: str) -> list[dict]:
        prompt = TASK_PLANNER_PROMPT.format(user_input=user_input)
        output = generate(prompt)
        cleaned_output = extract_json_block(output)

        try:
            tasks = json.loads(cleaned_output)

            if not isinstance(tasks, list):
                return []

            valid_tasks = []
            for item in tasks:
                if not isinstance(item, dict):
                    continue

                valid_tasks.append(
                    {
                        "task": item.get("task", "Untitled task"),
                        "priority": item.get("priority", "Medium"),
                        "urgency": item.get("urgency", "Normal"),
                        "reason": item.get("reason", "No reason provided."),
                    }
                )

            return valid_tasks

        except json.JSONDecodeError:
            return [
                {
                    "task": "Review request manually",
                    "priority": "High",
                    "urgency": "Urgent",
                    "reason": "The planner returned an invalid response.",
                }
            ]