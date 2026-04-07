from typing import Optional

from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    user_input: str = Field(..., min_length=1)


class TaskItem(BaseModel):
    task: str
    priority: str
    urgency: str
    reason: str
    estimated_duration: str
    energy_level: str
    best_time: str
    can_delegate: bool
    impact: str
    deadline_risk: str


class ScheduleItem(BaseModel):
    task: str
    start_time: str
    end_time: str
    focus: str


class SlideItem(BaseModel):
    title: str
    bullets: list[str]


class TaskPilotResponse(BaseModel):
    input: str
    tasks: list[TaskItem]
    schedule: list[ScheduleItem] = Field(default_factory=list)
    summary: Optional[str] = None
    slides: list[SlideItem] = Field(default_factory=list)
    visual: Optional[str] = None
    export_report: Optional[str] = None