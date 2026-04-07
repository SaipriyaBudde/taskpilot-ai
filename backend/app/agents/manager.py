from app.agents.content import ContentAgent
from app.agents.planner import TaskPlanner
from app.agents.presentation import PresentationAgent
from app.agents.scheduler import Scheduler
from app.agents.visuals import VisualAgent
from app.db.memory import get_context_string


class Manager:
    def __init__(self):
        self.planner = TaskPlanner()
        self.scheduler = Scheduler()
        self.content = ContentAgent()
        self.presentation = PresentationAgent()
        self.visuals = VisualAgent()

    def handle(self, user_input: str) -> dict:
        context = get_context_string()

        enriched_input = (
            f"{context}\n"
            f"Current request: {user_input}"
            if context
            else user_input
        )

        tasks = self.planner.run(enriched_input)
        schedule = self.scheduler.run(tasks)
        summary = self.content.run(enriched_input)
        slides = self.presentation.run(tasks, summary)
        visual = self.visuals.run(tasks, summary)

        return {
            "input": user_input,
            "tasks": tasks,
            "schedule": schedule,
            "summary": summary,
            "slides": slides,
            "visual": visual,
        }