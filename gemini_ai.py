# ============================================================
# gemini_ai.py (v4)
# AI Scheduler Agent
# Gemini API Wrapper
# ============================================================

import os
import json

import streamlit as st
import google.generativeai as genai

# ============================================================
# API KEY
# ============================================================

API_KEY = None

# Streamlit Cloud
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# Local (.env 또는 환경변수)
if API_KEY is None:
    API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = None

if API_KEY:

    genai.configure(api_key=API_KEY)

    MODEL = genai.GenerativeModel(
        "gemini-1.5-flash"
    )

# ============================================================
# MODE
# ============================================================

APP_MODE = "LIVE"
# LIVE
# FALLBACK
# DEMO

# ============================================================
# AI Call
# ============================================================

def ai_call(prompt, fallback=None):

    if APP_MODE == "DEMO":

        if fallback:
            return fallback()

        return ""

    if APP_MODE == "FALLBACK":

        if fallback:
            return fallback()

        return ""

    if MODEL is None:

        if fallback:
            return fallback()

        return ""

    try:

        response = MODEL.generate_content(prompt)

        return response.text

    except Exception:

        if fallback:
            return fallback()

        return ""

# ============================================================
# Replan Decision
# ============================================================

def decide_replan(schedule_summary, stress_score):

    def fallback():

        return stress_score >= 70

    prompt = f"""

당신은 AI 일정관리 Agent입니다.

현재 스트레스 점수는

{stress_score}

입니다.

현재 일정은 아래와 같습니다.

{schedule_summary}

재배치를 해야하면 YES

필요없으면 NO

반드시 YES 또는 NO만 답하세요.

"""

    result = ai_call(prompt, fallback)

    if isinstance(result, bool):

        return result

    result = str(result).upper()

    return "YES" in result

# ============================================================
# Schedule Explanation
# ============================================================

def explain_schedule(tasks, logs):

    def fallback():

        return (
            "마감일이 가까운 일정과 "
            "중요도가 높은 업무를 "
            "우선적으로 배치했습니다."
        )

    prompt = f"""

당신은 AI 일정관리 전문가입니다.

Task 목록

{tasks}

배치 결과

{logs}

사용자가 이해하기 쉽게

왜 이렇게 스케줄을 만들었는지

3줄 이내로 설명하세요.

"""

    return ai_call(prompt, fallback)

# ============================================================
# One Line Summary
# ============================================================

def one_line_summary(stress_score):

    def fallback():

        if stress_score >= 80:
            return "🔥 오늘은 과부하가 예상됩니다."

        if stress_score >= 60:
            return "☕ 중간 휴식을 추천합니다."

        if stress_score >= 40:
            return "🙂 균형 잡힌 일정입니다."

        return "😄 여유로운 하루입니다."

    prompt = f"""

스트레스 점수

{stress_score}

한 줄로 요약해주세요.

이모지를 포함해주세요.

"""

    return ai_call(prompt, fallback)

# ============================================================
# AI Thinking
# ============================================================

def generate_reasoning(tasks):

    def fallback():

        texts = []

        for task in tasks:

            texts.append(

                f"{task['name']}의 중요도와 "
                "마감일을 고려했습니다."

            )

        return "\n".join(texts)

    prompt = f"""

아래 업무를 분석하여

AI가 어떤 순서로 생각했는지

5단계 Thinking을 작성하세요.

Task

{tasks}

"""

    return ai_call(prompt, fallback)

# ============================================================
# AI Recommendation
# ============================================================

def recommend_action(stress_score):

    def fallback():

        if stress_score >= 85:

            return (
                "🚶 산책 후 다시 시작하는 것을 추천합니다."
            )

        if stress_score >= 70:

            return (
                "☕ 커피 한 잔과 10분 휴식을 추천합니다."
            )

        if stress_score >= 45:

            return (
                "🙂 현재 리듬을 유지하세요."
            )

        return (
            "😄 충분히 여유로운 일정입니다."
        )

    prompt = f"""

스트레스 점수는

{stress_score}

입니다.

한 줄 추천을 작성해주세요.

"""

    return ai_call(prompt, fallback)

# ============================================================
# AI JSON Replanner (향후 사용)
# ============================================================

def generate_replan_strategy(schedule, tasks):

    def fallback():

        return {

            "action": "KEEP",

            "reason": "Fallback"

        }

    prompt = f"""

당신은 AI Scheduling Agent입니다.

현재 일정

{schedule}

Task

{tasks}

JSON만 출력하세요.

형식

{{
    "action":"KEEP/SHIFT/SPLIT",
    "reason":"..."
}}

"""

    result = ai_call(prompt, fallback)

    if isinstance(result, dict):

        return result

    try:

        return json.loads(result)

    except Exception:

        return fallback()