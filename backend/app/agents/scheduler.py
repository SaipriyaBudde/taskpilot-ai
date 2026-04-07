import json

from app.core.llm_client import extract_json_block, generate
from app.core.prompts import SCHEDULER_PROMPT


class Scheduler:
    def run(self, tasks: list[dict]) -> list[dict]:
        if not tasks:
            return []

        prompt = SCHEDULER_PROMPT.format(tasks=json.dumps(tasks, indent=2))
        output = generate(prompt)
        cleaned_output = extract_json_block(output)

        try:
            schedule = json.loads(cleaned_output)

            if not isinstance(schedule, list):
                return []

            valid_schedule = []
            for item in schedule:
                if not isinstance(item, dict):
                    continue

                valid_schedule.append(
                    {
                        "task": item.get("task", "Untitled task"),
                        "start_time": item.get("start_time", "09:00 AM"),
                        "end_time": item.get("end_time", "10:00 AM"),
                        "focus": item.get("focus", "Focused work session"),
                    }
                )

            return valid_schedule

        except json.JSONDecodeError:
            return []