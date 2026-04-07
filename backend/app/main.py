from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import re

app = FastAPI(title="TaskPilot AI Backend")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon demo; tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    user_input: str


@app.get("/")
def root():
    return {"message": "TaskPilot AI backend is running."}


@app.post("/run")
def run_taskpilot(payload: UserInput):
    text = payload.user_input.lower()

    # --- basic intelligent extraction ---
    tasks = []

    if "deadline" in text or "project" in text:
        tasks.append({
            "task": "Complete project deliverable",
            "priority": "High",
            "urgency": "Urgent",
            "reason": "This appears to be your most time-sensitive and high-impact responsibility.",
            "estimated_duration": "2 hrs",
            "energy_level": "High",
            "best_time": "Morning Deep Work",
            "impact": "High",
            "deadline_risk": "High",
            "can_delegate": False
        })

    if "interview" in text or "prepare" in text:
        tasks.append({
            "task": "Prepare for interview / key preparation task",
            "priority": "High",
            "urgency": "Medium",
            "reason": "Preparation creates future leverage and improves your confidence and readiness.",
            "estimated_duration": "1.5 hrs",
            "energy_level": "High",
            "best_time": "Late Morning",
            "impact": "High",
            "deadline_risk": "Medium",
            "can_delegate": False
        })

    if "grocery" in text or "groceries" in text or "buy" in text:
        tasks.append({
            "task": "Buy groceries / run personal errands",
            "priority": "Medium",
            "urgency": "Low",
            "reason": "This is important for personal maintenance, but not your highest cognitive priority.",
            "estimated_duration": "45 mins",
            "energy_level": "Low",
            "best_time": "Evening",
            "impact": "Medium",
            "deadline_risk": "Low",
            "can_delegate": True
        })

    if "office" in text or "work" in text or "meeting" in text or "tasks" in text:
        tasks.append({
            "task": "Clear pending office/admin tasks",
            "priority": "Medium",
            "urgency": "Medium",
            "reason": "Reducing admin backlog prevents mental clutter and protects focus for bigger work.",
            "estimated_duration": "1 hr",
            "energy_level": "Medium",
            "best_time": "Afternoon",
            "impact": "Medium",
            "deadline_risk": "Medium",
            "can_delegate": False
        })

    # fallback if no obvious tasks detected
    if not tasks:
        tasks = [
            {
                "task": "Clarify and break down your workload",
                "priority": "High",
                "urgency": "Medium",
                "reason": "Your input needs to be translated into a more structured action plan first.",
                "estimated_duration": "30 mins",
                "energy_level": "Medium",
                "best_time": "Morning",
                "impact": "High",
                "deadline_risk": "Medium",
                "can_delegate": False
            },
            {
                "task": "Execute the highest-value item first",
                "priority": "High",
                "urgency": "High",
                "reason": "Starting with the most important task creates momentum and reduces anxiety.",
                "estimated_duration": "90 mins",
                "energy_level": "High",
                "best_time": "Morning Deep Work",
                "impact": "High",
                "deadline_risk": "High",
                "can_delegate": False
            }
        ]

    schedule = []
    time_slots = [
        ("09:00 AM", "10:30 AM"),
        ("10:45 AM", "12:15 PM"),
        ("01:30 PM", "02:30 PM"),
        ("03:00 PM", "04:00 PM"),
        ("06:00 PM", "07:00 PM"),
    ]

    for i, task in enumerate(tasks[:5]):
        schedule.append({
            "start_time": time_slots[i][0],
            "end_time": time_slots[i][1],
            "task": task["task"],
            "focus": f"Focused execution block for: {task['task']}"
        })

    summary = (
        "Your day should begin with high-impact cognitive work first, "
        "followed by medium-effort operational tasks, and end with lighter personal execution. "
        "This plan is designed to reduce overwhelm while preserving momentum."
    )

    visual = (
        "Think of your day as a runway: launch your hardest work early, "
        "stabilize with admin and coordination in the middle, and land with low-energy errands."
    )

    export_report = f"""
TASKPILOT AI — EXECUTION REPORT

USER INPUT:
{payload.user_input}

EXECUTIVE SUMMARY:
{summary}

TOP TASKS:
""" + "\n".join(
        [f"- {task['task']} ({task['priority']} Priority, {task['urgency']} Urgency)" for task in tasks]
    ) + """

SCHEDULE:
""" + "\n".join(
        [f"- {item['start_time']} to {item['end_time']}: {item['task']}" for item in schedule]
    ) + f"""

VISUAL STRATEGY:
{visual}
"""

    slides = [
        {
            "title": "Problem: Mental Overload",
            "bullets": [
                "Users often struggle with competing priorities",
                "Decision fatigue reduces execution quality",
                "Task chaos leads to missed momentum"
            ]
        },
        {
            "title": "Solution: TaskPilot AI",
            "bullets": [
                "Transforms messy input into clear priorities",
                "Builds energy-aware execution plans",
                "Provides strategic insights, not just task lists"
            ]
        },
        {
            "title": "Execution Output",
            "bullets": [
                "Priority-ranked tasks",
                "AI-generated schedule",
                "Shareable executive summary"
            ]
        }
    ]

    return {
        "summary": summary,
        "tasks": tasks,
        "schedule": schedule,
        "visual": visual,
        "export_report": export_report,
        "slides": slides
    }