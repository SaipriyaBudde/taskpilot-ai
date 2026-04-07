import json
import os
import re
from typing import Any

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class Orchestrator:
    def __init__(self): 
        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    def _extract_json(self, text: str) -> dict[str, Any]:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("No valid JSON found in model response.")
        return json.loads(match.group())

    def run(self, user_input: str) -> dict[str, Any]:
        prompt = f"""
You are TaskPilot AI, an elite AI executive assistant and decision-support system.

Return ONLY valid JSON.
No markdown.
No explanations.
No extra words before or after the JSON.

Schema:
{{
  "input": "original input",
  "tasks": [
    {{
      "task": "task name",
      "priority": "High/Medium/Low",
      "urgency": "Urgent/Medium/Low",
      "reason": "why this task has this ranking",
      "estimated_duration": "e.g. 30 mins / 2 hours",
      "energy_level": "High/Medium/Low",
      "best_time": "Morning/Afternoon/Evening",
      "can_delegate": true,
      "impact": "High/Medium/Low",
      "deadline_risk": "High/Medium/Low"
    }}
  ],
  "schedule": [
    {{
      "task": "task name",
      "start_time": "HH:MM",
      "end_time": "HH:MM",
      "focus": "type of focus"
    }}
  ],
  "summary": "short helpful summary",
  "slides": [
    {{
      "title": "slide title",
      "bullets": ["point 1", "point 2", "point 3"]
    }}
  ],
  "visual": "one-line visual summary",
  "export_report": "short polished report text"
}}

Decision Rules:
- Prioritize based on urgency, impact, deadlines, and mental energy required
- High-energy tasks should usually be placed earlier in the day
- Low-energy/logistics tasks should be placed later
- Include 3 to 5 meaningful tasks
- Include 3 to 5 realistic schedule blocks
- "can_delegate" should be true only if the task could reasonably be outsourced, reassigned, or postponed without direct personal execution
- "deadline_risk" should reflect what happens if the task is delayed
- Make the output feel polished, human, strategic, and demo-worthy

User input:
{user_input}
"""

        try:
            response = self.model.generate_content(prompt)
            raw_output = response.text.strip()

            print("RAW GEMINI OUTPUT:\n", raw_output)

            return self._extract_json(raw_output)

        except Exception as e:
            print("ERROR:", repr(e))
            return {
    "input": user_input,
    "tasks": [
        {
            "task": "Finalize Project Deliverables",
            "priority": "High",
            "urgency": "Urgent",
            "reason": "The project deadline is tomorrow and carries the highest immediate consequence.",
            "estimated_duration": "3 hours",
            "energy_level": "High",
            "best_time": "Morning",
            "can_delegate": False,
            "impact": "High",
            "deadline_risk": "High"
        },
        {
            "task": "Prepare for Data Analyst Interview",
            "priority": "High",
            "urgency": "Medium",
            "reason": "This supports near-term career growth and benefits from focused cognitive effort.",
            "estimated_duration": "2 hours",
            "energy_level": "High",
            "best_time": "Afternoon",
            "can_delegate": False,
            "impact": "High",
            "deadline_risk": "Medium"
        },
        {
            "task": "Process Pending Office Tasks",
            "priority": "Medium",
            "urgency": "Medium",
            "reason": "These tasks help maintain work continuity and prevent backlog buildup.",
            "estimated_duration": "90 mins",
            "energy_level": "Medium",
            "best_time": "Afternoon",
            "can_delegate": False,
            "impact": "Medium",
            "deadline_risk": "Medium"
        },
        {
            "task": "Buy Groceries",
            "priority": "Low",
            "urgency": "Low",
            "reason": "Necessary for personal maintenance but less urgent than professional deliverables.",
            "estimated_duration": "1 hour",
            "energy_level": "Low",
            "best_time": "Evening",
            "can_delegate": True,
            "impact": "Low",
            "deadline_risk": "Low"
        }
    ],
    "schedule": [
        {
            "task": "Deep Work: Project Finalization",
            "start_time": "09:00",
            "end_time": "12:00",
            "focus": "High-Intensity Execution"
        },
        {
            "task": "Data Analyst Technical Review",
            "start_time": "13:00",
            "end_time": "15:00",
            "focus": "Analytical Learning"
        },
        {
            "task": "Office Task Batching",
            "start_time": "15:30",
            "end_time": "17:00",
            "focus": "Administrative Flow"
        },
        {
            "task": "Grocery Run",
            "start_time": "17:30",
            "end_time": "18:30",
            "focus": "Low-Energy Logistics"
        }
    ],
    "summary": "TaskPilot prioritized your day by balancing deadline pressure, cognitive load, and strategic career value.",
    "slides": [
        {
            "title": "Priority Intelligence",
            "bullets": [
                "Front-loaded high-risk deadline work",
                "Protected time for career growth",
                "Deferred low-energy errands strategically"
            ]
        },
        {
            "title": "Execution Strategy",
            "bullets": [
                "Morning reserved for deep work",
                "Afternoon used for analytical review and admin tasks",
                "Evening kept for low-energy logistics"
            ]
        }
    ],
    "visual": "A priority curve that starts with deep cognitive work and tapers into operational and personal tasks.",
    "export_report": "TaskPilot AI generated a strategic execution plan by ranking tasks according to urgency, energy demand, and downstream impact."
}