# ============================================================
# app.py (v4)
# AI Scheduler Agent UI
# Streamlit Entry Point
# ============================================================

import streamlit as st

from scheduler import agent_optimize
from stress import flatten_week, analyze_schedule, recommend_break, summary_text
from decision_engine import generate_reasoning, overall_comment
from demo_engine import run_demo
from random_schedule import generate_base_week
from gemini_ai import (
    decide_replan,
    explain_schedule,
    one_line_summary,
    recommend_action,
    APP_MODE
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Scheduler Agent v4",
    layout="wide"
)

st.title("🧠 AI Scheduler Agent v4")

# ============================================================
# SESSION STATE
# ============================================================

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ============================================================
# TASK INPUT UI
# ============================================================

st.subheader("📌 Task 입력")

col1, col2, col3, col4 = st.columns(4)

with col1:
    name = st.text_input("Task Name")

with col2:
    deadline = st.number_input("Deadline", 1, 7, 3)

with col3:
    importance = st.number_input("Importance", 1, 5, 3)

with col4:
    difficulty = st.number_input("Difficulty", 1, 5, 3)

duration = st.slider("Duration (hours)", 1, 4, 2)

if st.button("➕ Add Task"):

    st.session_state.tasks.append({

        "name": name,

        "deadline": deadline,

        "importance": importance,

        "difficulty": difficulty,

        "duration": duration

    })

st.write("현재 Task:", st.session_state.tasks)

# ============================================================
# MODE SELECTOR
# ============================================================

mode = st.sidebar.selectbox(
    "MODE",
    ["LIVE", "FALLBACK", "DEMO"]
)

APP_MODE = mode

st.sidebar.write("Current Mode:", APP_MODE)

# ============================================================
# BASE WEEK
# ============================================================

base_week = generate_base_week()

# ============================================================
# RUN BUTTON
# ============================================================

if st.button("🚀 RUN AI AGENT"):

    st.subheader("📅 Base Schedule")

    st.json(base_week)

    # ========================================================
    # DEMO MODE
    # ========================================================

    if APP_MODE == "DEMO":

        result = run_demo(st.session_state.tasks)

        st.subheader("🤖 AI Result (DEMO)")

        st.json(result)

        st.stop()

    # ========================================================
    # LIVE / FALLBACK MODE
    # ========================================================
        # ============================================================
    # AI AGENT EXECUTION
    # ============================================================

    def reflect_fn(week):

        flat = flatten_week(week)

        result = analyze_schedule(flat)

        return result["score"]

    def replan_fn(stress):

        return decide_replan({}, stress)

    # ============================================================
    # RUN AGENT
    # ============================================================

    optimized_week, logs, history = agent_optimize(

        st.session_state.tasks,

        base_week,

        reflect_fn=reflect_fn,

        replan_fn=replan_fn

    )

    # ============================================================
    # STRESS ANALYSIS
    # ============================================================

    flat = flatten_week(optimized_week)

    stress_result = analyze_schedule(flat)

    stress_score = stress_result["score"]

    daily = stress_result["daily"]

    # ============================================================
    # OUTPUT - SCHEDULE
    # ============================================================

    st.subheader("📅 Optimized Schedule")

    st.json(optimized_week)

    # ============================================================
    # OUTPUT - STRESS
    # ============================================================

    st.subheader("📊 Stress Analysis")

    st.write("Total Score:", stress_score)

    st.json(daily)

    st.write(summary_text({"score": stress_score}))

    st.write("Break Recommendation:")

    st.write(recommend_break(stress_score))

    # ============================================================
    # OUTPUT - HISTORY
    # ============================================================

    st.subheader("🔁 Replan History")

    st.json(history)

    # ============================================================
    # OUTPUT - LOGS
    # ============================================================

    st.subheader("🧾 Scheduling Logs")

    st.json(logs)
        # ============================================================
    # AI REASONING (Decision Engine)
    # ============================================================

    st.subheader("🧠 AI Reasoning")

    reasoning_logs = generate_reasoning(st.session_state.tasks)

    st.json(reasoning_logs)

    # ============================================================
    # AI EXPLANATION (Gemini or fallback)
    # ============================================================

    st.subheader("📝 AI Explanation")

    explanation = explain_schedule(
        st.session_state.tasks,
        logs
    )

    st.write(explanation)

    # ============================================================
    # OVERALL COMMENT
    # ============================================================

    st.subheader("📌 Overall AI Comment")

    comment = overall_comment(stress_score)

    st.write(comment)

    # ============================================================
    # ONE LINE SUMMARY
    # ============================================================

    st.subheader("⚡ One-line Summary")

    summary = one_line_summary(stress_score)

    st.write(summary)

    # ============================================================
    # RECOMMENDATION (Gemini or fallback)
    # ============================================================

    st.subheader("💡 Recommendation")

    recommendation = recommend_action(stress_score)

    st.write(recommendation)

    # ============================================================
    # FINAL DEBUG INFO
    # ============================================================

    with st.expander("🔧 Debug Info"):

        st.write("Mode:", APP_MODE)

        st.write("Task Count:", len(st.session_state.tasks))

        st.write("Stress Score:", stress_score)

        st.write("History:", history)

    # ============================================================
    # END
    # ============================================================