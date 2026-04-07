import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/run"

st.set_page_config(
    page_title="TaskPilot AI",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        .hero-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .hero-subtitle {
            font-size: 1rem;
            color: #6b7280;
            margin-bottom: 2rem;
        }

        .metric-card {
            padding: 1rem 1.2rem;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            background: #ffffff;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
            text-align: center;
        }

        .metric-label {
            font-size: 0.9rem;
            color: #6b7280;
            margin-bottom: 0.4rem;
        }

        .metric-value {
            font-size: 1.6rem;
            font-weight: 700;
        }

        .section-card {
            padding: 1.2rem;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            background: #ffffff;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
            margin-bottom: 1rem;
        }

        .section-title {
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 0.7rem;
        }

        .small-muted {
            font-size: 0.92rem;
            color: #6b7280;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_tasks(tasks: list[dict]) -> None:
    if not tasks:
        st.info("No tasks generated.")
        return

    for index, task in enumerate(tasks, start=1):
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">{index}. {task.get("task", "Untitled task")}</div>
                <div><strong>Priority:</strong> {task.get("priority", "Medium")}</div>
                <div><strong>Urgency:</strong> {task.get("urgency", "Normal")}</div>
                <div style="margin-top: 0.5rem;"><strong>Why it matters:</strong> {task.get("reason", "No reason provided.")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_schedule(schedule: list[dict]) -> None:
    if not schedule:
        st.info("No schedule generated.")
        return

    for block in schedule:
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">{block.get("task", "Untitled task")}</div>
                <div><strong>Time:</strong> {block.get("start_time", "09:00 AM")} → {block.get("end_time", "10:00 AM")}</div>
                <div style="margin-top: 0.5rem;"><strong>Focus:</strong> {block.get("focus", "Focused work session")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_slides(slides: list[dict]) -> None:
    if not slides:
        st.info("No slide content generated.")
        return

    for slide in slides:
        bullets = "".join(
            f"<li>{bullet}</li>" for bullet in slide.get("bullets", [])
        )

        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">{slide.get("title", "Untitled Slide")}</div>
                <ul style="margin-top: 0.5rem;">
                    {bullets}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def build_exec_summary(data: dict) -> str:
    task_count = len(data.get("tasks", []))
    schedule_count = len(data.get("schedule", []))
    slide_count = len(data.get("slides", []))

    summary = data.get("summary") or "No written summary was generated."

    return (
        f"TaskPilot identified {task_count} actionable task(s), generated "
        f"{schedule_count} schedule block(s), and prepared {slide_count} "
        f"presentation slide draft(s).\n\n{summary}"
    )


left, right = st.columns([1.5, 1])

with left:
    st.markdown('<div class="hero-title">🧠 TaskPilot AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Multi-Agent Productivity Assistant for turning messy work into structured execution.</div>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Why it matters</div>
            <div class="small-muted">
                TaskPilot acts like an AI Chief of Staff — breaking down work,
                scheduling execution, and generating useful outputs in one flow.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### What do you need help organizing today?")

user_input = st.text_area(
    label="",
    placeholder="Example: Tomorrow I need to prepare for a client call, summarize my meeting notes, create a slide for the weekly review, and plan my workday.",
    height=180,
)

run_button = st.button("Run TaskPilot", use_container_width=True)

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "history" not in st.session_state:
    st.session_state.history = []

if run_button:
    if not user_input.strip():
        st.warning("Please enter a task request.")
    else:
        with st.spinner("TaskPilot is organizing your work..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"user_input": user_input},
                    timeout=180,
                )
                response.raise_for_status()
                data = response.json()

                st.session_state.last_result = data
                st.session_state.history.insert(0, user_input.strip())
                st.session_state.history = st.session_state.history[:5]

                st.success("Plan generated successfully.")

            except requests.RequestException as error:
                st.error("Could not connect to the backend.")
                st.caption(str(error))

data = st.session_state.last_result

if data:
    st.markdown("## Execution Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Tasks</div>
                <div class="metric-value">{len(data.get("tasks", []))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Schedule Blocks</div>
                <div class="metric-value">{len(data.get("schedule", []))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Slides Drafted</div>
                <div class="metric-value">{len(data.get("slides", []))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    left_panel, right_panel = st.columns([2, 1])

    with left_panel:
        st.markdown("### Chief of Staff Summary")
        st.markdown(
            f"""
            <div class="section-card">
                {build_exec_summary(data).replace("\n", "<br><br>")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_panel:
        st.markdown("### Recent Requests")

        if st.session_state.history:
            for item in st.session_state.history:
                st.markdown(
                    f"""
                    <div class="section-card">
                        <div class="small-muted">{item}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No recent requests yet.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Tasks", "Schedule", "Summary & Visual", "Slides", "Export"]
    )

    with tab1:
        render_tasks(data.get("tasks", []))

    with tab2:
        render_schedule(data.get("schedule", []))

    with tab3:
        st.markdown("### Work Summary")
        st.markdown(
            f"""
            <div class="section-card">
                {data.get("summary") or "No summary generated."}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Visual Concept")
        st.markdown(
            f"""
            <div class="section-card">
                {data.get("visual") or "No visual concept generated."}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab4:
        render_slides(data.get("slides", []))

    with tab5:
    st.markdown("### Shareable Work Plan")
    st.markdown(
        """
        <div class="small-muted">
            Copy this structured work plan for notes, updates, or sharing.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_area(
        label="Export Report",
        value=data.get("export_report") or "No export report available.",
        height=450,
    )