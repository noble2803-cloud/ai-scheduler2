# ============================================================
# app.py
# AI Scheduler Agent v5
# Part 1 / 3
# ============================================================

import streamlit as st
import pandas as pd
import time

from scheduler import agent_optimize
from stress import (
    flatten_week,
    analyze_schedule,
    recommend_break,
    summary_text
)

from random_schedule import generate_base_week

from decision_engine import (
    generate_reasoning,
    overall_comment
)

from gemini_ai import (
    decide_replan,
    explain_schedule,
    one_line_summary,
    recommend_action,
    APP_MODE
)

from demo_engine import run_demo


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="AI Scheduler Agent",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Scheduler Agent")

st.caption("AI가 사용자의 업무를 분석하여 최적의 일정을 생성합니다.")

# ============================================================
# SESSION
# ============================================================

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "result" not in st.session_state:
    st.session_state.result = None

# ============================================================
# SIDEBAR
# ============================================================

mode = st.sidebar.selectbox(

    "AI Mode",

    [

        "LIVE",

        "FALLBACK",

        "DEMO"

    ]

)

APP_MODE = mode

st.sidebar.success(f"Current Mode : {APP_MODE}")

# ============================================================
# INPUT
# ============================================================

st.subheader("📌 일정 추가")

c1,c2,c3,c4 = st.columns(4)

with c1:

    task_name = st.text_input("일정 이름")

with c2:

    deadline = st.selectbox(

        "마감일",

        [1,2,3,4,5,6,7]

    )

with c3:

    importance = st.slider(

        "중요도",

        1,

        5,

        3

    )

with c4:

    difficulty = st.slider(

        "업무강도",

        1,

        5,

        3

    )

duration = st.slider(

    "소요시간",

    1,

    4,

    2

)

# ============================================================
# BUTTON
# ============================================================

if st.button("➕ 일정 추가"):

    if task_name.strip()=="":

        st.warning("일정 이름을 입력하세요.")

    else:

        st.session_state.tasks.append({

            "name":task_name,

            "deadline":deadline,

            "importance":importance,

            "difficulty":difficulty,

            "duration":duration

        })

# ============================================================
# TASK LIST
# ============================================================

st.subheader("📋 입력된 일정")

if len(st.session_state.tasks)==0:

    st.info("추가된 일정이 없습니다.")

else:

    remove=None

    for i,task in enumerate(st.session_state.tasks):

        col1,col2=st.columns([9,1])

        with col1:

            st.write(
                f"**{task['name']}** | "
                f"마감:{task['deadline']}일 "
                f"| 중요:{task['importance']} "
                f"| 강도:{task['difficulty']} "
                f"| {task['duration']}시간"
            )

        with col2:

            if st.button("삭제",key=f"del{i}"):

                remove=i

    if remove is not None:

        st.session_state.tasks.pop(remove)

        st.rerun()

# ============================================================
# RUN
# ============================================================

run = st.button("🚀 AI 스케줄 생성")

# ============================================================
# RUN AGENT
# ============================================================

if run:

    # --------------------------------------------------------
    # 기존 일정 생성
    # --------------------------------------------------------

    base_week = generate_base_week()

    # --------------------------------------------------------
    # DEMO MODE
    # --------------------------------------------------------

    if APP_MODE == "DEMO":

        demo = run_demo(st.session_state.tasks)

        st.session_state.result = {

            "week": base_week,

            "logs": [],

            "history": demo["history"],

            "thinking": demo["thinking"],

            "stress": {

                "score": demo["stress"],

                "daily": {}

            },

            "demo": demo

        }

    else:

        # --------------------------------------------------------
        # Reflect Function
        # --------------------------------------------------------

        def reflect_fn(week):

            flat = flatten_week(week)

            result = analyze_schedule(flat)

            return result["score"]

        # --------------------------------------------------------
        # Replan Function
        # --------------------------------------------------------

        def replan_fn(score):

            return decide_replan({}, score)

        # --------------------------------------------------------
        # AI Thinking Animation
        # --------------------------------------------------------

        status = st.empty()

        progress = st.progress(0)

        steps = [

            "📅 기존 스케줄 분석",

            "🧠 업무 우선순위 계산",

            "📊 스트레스 예측",

            "♻️ 일정 재배치",

            "✅ 최종 스케줄 생성"

        ]

        for i, step in enumerate(steps):

            status.info(step)

            progress.progress((i + 1) / len(steps))

            time.sleep(0.35)

        status.success("AI 일정 생성 완료")

        # --------------------------------------------------------
        # Agent
        # --------------------------------------------------------

        optimized_week, logs, history = agent_optimize(

            st.session_state.tasks,

            base_week,

            reflect_fn=reflect_fn,

            replan_fn=replan_fn

        )

        flat = flatten_week(optimized_week)

        stress = analyze_schedule(flat)

        thinking = generate_reasoning(

            st.session_state.tasks

        )

        st.session_state.result = {

            "week": optimized_week,

            "logs": logs,

            "history": history,

            "thinking": thinking,

            "stress": stress

        }

# ============================================================
# OUTPUT
# ============================================================

if st.session_state.result is not None:

    result = st.session_state.result

    week = result["week"]

    stress = result["stress"]

    score = stress["score"]

    daily = stress["daily"]

    st.divider()

    st.header("📅 AI 최적화 결과")

    day_name = {

        "Monday":"월요일",

        "Tuesday":"화요일",

        "Wednesday":"수요일",

        "Thursday":"목요일",

        "Friday":"금요일",

        "Saturday":"토요일",

        "Sunday":"일요일"

    }

    for day in week:

        st.subheader(f"🗓️ {day_name[day]}")

        rows=[]

        schedules=sorted(

            week[day],

            key=lambda x:x["start"]

        )

        for item in schedules:

            rows.append({

                "시간":

                f"{item['start']:02d}:00 ~ {item['end']:02d}:00",

                "일정":item["task"],

                "종류":item["type"]

            })

        if len(rows)==0:

            st.info("일정 없음")

        else:

            df=pd.DataFrame(rows)

            st.dataframe(

                df,

                hide_index=True,

                use_container_width=True

            )


    # ============================================================
    # Stress Dashboard
    # ============================================================

    st.divider()
    st.header("🧠 AI Stress Dashboard")

    st.metric(
        "Stress Score",
        f"{score:.1f}"
    )

    st.progress(min(score / 100.0, 1.0))

    if score >= 80:
        st.error("🔥 매우 높은 스트레스가 예상됩니다.")
    elif score >= 60:
        st.warning("⚠️ 휴식을 권장합니다.")
    elif score >= 40:
        st.info("🙂 적절한 업무량입니다.")
    else:
        st.success("😄 여유로운 일정입니다.")

    # summary_text가 level을 요구하는 기존 버전도 동작하도록 보정
    level = (
        "매우 높음" if score >= 80 else
        "높음" if score >= 60 else
        "보통" if score >= 40 else
        "낮음"
    )

    st.write(
        summary_text({
            "score": score,
            "level": level
        })
    )

    st.write("### ☕ AI 휴식 추천")
    st.success(recommend_break(score))

    # ============================================================
    # Daily Stress
    # ============================================================

    if daily:

        st.subheader("📈 요일별 스트레스")

        daily_df = pd.DataFrame(
            [
                {
                    "요일": k,
                    "Stress": v
                }
                for k, v in daily.items()
            ]
        )

        st.bar_chart(
            daily_df.set_index("요일")
        )

    # ============================================================
    # AI Reasoning
    # ============================================================

    st.divider()

    st.header("🧠 AI Thinking")

    thinking = result.get("thinking", [])

    if isinstance(thinking, str):

        st.write(thinking)

    elif isinstance(thinking, list):

        for t in thinking:

            st.write("•", t)

    # ============================================================
    # Gemini Explanation
    # ============================================================

    st.divider()

    st.header("🤖 AI Explanation")

    try:

        explain = explain_schedule(

            st.session_state.tasks,

            result["logs"]

        )

        st.success(explain)

    except Exception as e:

        st.warning(f"Fallback 설명 사용 ({e})")

    # ============================================================
    # Overall Comment
    # ============================================================

    st.subheader("📌 Overall Comment")

    st.info(
        overall_comment(score)
    )

    # ============================================================
    # One Line Summary
    # ============================================================

    st.subheader("⚡ One-line Summary")

    try:

        st.success(
            one_line_summary(score)
        )

    except:

        pass

    # ============================================================
    # Recommendation
    # ============================================================

    st.subheader("💡 AI Recommendation")

    try:

        st.write(
            recommend_action(score)
        )

    except:

        pass

    # ============================================================
    # Replan History
    # ============================================================

    st.divider()

    st.header("🔄 Replan History")

    if len(result["history"]) == 0:

        st.info("Replan 없음")

    else:

        st.json(result["history"])

    # ============================================================
    # Scheduling Logs
    # ============================================================

    st.header("📜 Scheduling Log")

    if len(result["logs"]) == 0:

        st.info("Log 없음")

    else:

        st.json(result["logs"])

    # ============================================================
    # Debug
    # ============================================================

    with st.expander("🔧 Debug"):

        st.write("Mode :", APP_MODE)

        st.write("Tasks")

        st.json(st.session_state.tasks)

        st.write("Stress")

        st.json(stress)

        st.write("History")

        st.json(result["history"])

        st.write("Logs")

        st.json(result["logs"])
