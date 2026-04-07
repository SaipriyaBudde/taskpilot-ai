from app.db.base import MemoryEntry, SessionLocal


def save_entry(user_input: str, output: str) -> None:
    session = SessionLocal()

    try:
        entry = MemoryEntry(
            user_input=user_input,
            output=output,
        )
        session.add(entry)
        session.commit()
    finally:
        session.close()


def get_recent_entries(limit: int = 5) -> list[dict]:
    session = SessionLocal()

    try:
        entries = (
            session.query(MemoryEntry)
            .order_by(MemoryEntry.id.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": entry.id,
                "user_input": entry.user_input,
                "output": entry.output,
            }
            for entry in entries
        ]
    finally:
        session.close()

def get_context_string(limit: int = 3) -> str:
    entries = get_recent_entries(limit=limit)

    if not entries:
        return ""

    context_blocks = []

    for entry in entries:
        context_blocks.append(
            f"User previously asked: {entry['user_input']}\n"
        )

    return "\n".join(context_blocks)