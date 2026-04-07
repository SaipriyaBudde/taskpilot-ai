def build_export_report(result: dict) -> str:
    lines = []

    lines.append("TaskPilot Work Plan")
    lines.append("=" * 24)
    lines.append("")

    lines.append("Request")
    lines.append("-" * 7)
    lines.append(result.get("input", ""))
    lines.append("")

    tasks = result.get("tasks", [])
    if tasks:
        lines.append("Action Items")
        lines.append("-" * 12)
        for task in tasks:
            lines.append(
                f"- {task.get('task', 'Untitled task')} "
                f"({task.get('priority', 'Medium')} / {task.get('urgency', 'Normal')})"
            )
        lines.append("")

    schedule = result.get("schedule", [])
    if schedule:
        lines.append("Suggested Schedule")
        lines.append("-" * 18)
        for block in schedule:
            lines.append(
                f"- {block.get('start_time', '')} to {block.get('end_time', '')} | "
                f"{block.get('task', 'Untitled task')} — {block.get('focus', '')}"
            )
        lines.append("")

    summary = result.get("summary")
    if summary:
        lines.append("Summary")
        lines.append("-" * 7)
        lines.append(summary)
        lines.append("")

    slides = result.get("slides", [])
    if slides:
        lines.append("Slide Draft")
        lines.append("-" * 11)
        for index, slide in enumerate(slides, start=1):
            lines.append(f"Slide {index}: {slide.get('title', 'Untitled Slide')}")
            for bullet in slide.get("bullets", []):
                lines.append(f"  - {bullet}")
            lines.append("")
    
    visual = result.get("visual")
    if visual:
        lines.append("Visual Concept")
        lines.append("-" * 14)
        lines.append(visual)
        lines.append("")

    return "\n".join(lines).strip()