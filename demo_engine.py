# ============================================================
# demo_engine.py (v4)
# 발표용 Demo Mode
# API 없이도 AI처럼 동작하는 시뮬레이션
# ============================================================

import random
from copy import deepcopy

# ============================================================
# 발표 시나리오
# ============================================================

SCENARIOS = [

    {
        "name": "Busy Week",
        "stress": 82,
        "replan": True,
        "comment": "업무 과부하 감지"
    },

    {
        "name": "Balanced Week",
        "stress": 58,
        "replan": False,
        "comment": "균형 잡힌 일정"
    },

    {
        "name": "Relax Week",
        "stress": 32,
        "replan": False,
        "comment": "여유로운 일정"
    }

]

# ============================================================
# 랜덤 선택
# ============================================================

def choose_demo():

    return random.choice(SCENARIOS)

# ============================================================
# Thinking Log
# ============================================================

def create_thinking(tasks):

    logs = []

    for task in tasks:

        logs.append(

            f"[분석] '{task['name']}'의 중요도와 "
            f"마감일을 고려하여 우선순위를 계산했습니다."

        )

        if task["importance"] >= 4:

            logs.append(

                f"[판단] '{task['name']}'는 중요도가 높아 "
                "오전에 배치하는 것이 효율적입니다."

            )

        if task["difficulty"] >= 4:

            logs.append(

                f"[판단] '{task['name']}'는 난이도가 높아 "
                "집중도가 높은 시간대를 선택했습니다."

            )

    return logs

# ============================================================
# AI 설명
# ============================================================

def create_explanation(tasks):

    if len(tasks) == 0:

        return "입력된 일정이 없습니다."

    highest = sorted(

        tasks,

        key=lambda x: (
            x["importance"],
            -x["deadline"],
            x["difficulty"]
        ),

        reverse=True

    )[0]

    return (

        f"'{highest['name']}' 일정은 "
        "가장 높은 우선순위로 판단되어 "
        "가용 시간이 가장 많은 날짜에 먼저 배치되었습니다."

    )

# ============================================================
# History
# ============================================================

def create_history(stress):

    history = []

    history.append({

        "step": 1,

        "action": "초기 스케줄 생성",

        "stress": stress + 12

    })

    if stress >= 70:

        history.append({

            "step": 2,

            "action": "AI 재계획 수행",

            "stress": stress

        })

    else:

        history.append({

            "step": 2,

            "action": "재계획 불필요",

            "stress": stress

        })

    return history

# ============================================================
# 추천 휴식
# ============================================================

def recommend_break(stress):

    if stress >= 85:

        return random.choice([

            "☕ 커피 한 잔",

            "🚶 15분 산책",

            "🧘 스트레칭"

        ])

    elif stress >= 70:

        return random.choice([

            "🍪 간식",

            "☕ 티타임",

            "🌿 잠깐 환기"

        ])

    elif stress >= 45:

        return "🙂 현재 페이스를 유지하세요."

    return "😄 충분히 여유로운 하루입니다."

# ============================================================
# Demo Mode 실행
# ============================================================

def run_demo(tasks):

    scenario = choose_demo()

    return {

        "mode": "DEMO",

        "scenario": scenario["name"],

        "stress": scenario["stress"],

        "thinking": create_thinking(tasks),

        "history": create_history(

            scenario["stress"]

        ),

        "comment": scenario["comment"],

        "recommendation": recommend_break(

            scenario["stress"]

        ),

        "explanation": create_explanation(

            tasks

        )

    }