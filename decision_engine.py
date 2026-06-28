# ============================================================
# decision_engine.py (v4)
# AI Scheduler Agent - Decision Layer
# ============================================================

from copy import deepcopy

# ============================================================
# 중요도 계산
# ============================================================

def calculate_task_score(task):

    urgency = (8 - task["deadline"]) * 15
    importance = task["importance"] * 12
    difficulty = task["difficulty"] * 8
    duration = task["duration"] * 5

    return urgency + importance + difficulty + duration


# ============================================================
# Task 분석
# ============================================================

def analyze_tasks(tasks):

    analyzed = []

    for task in tasks:

        t = deepcopy(task)

        score = calculate_task_score(task)

        t["score"] = score

        if score >= 130:

            t["category"] = "Critical"

        elif score >= 100:

            t["category"] = "Important"

        elif score >= 70:

            t["category"] = "Normal"

        else:

            t["category"] = "Low"

        analyzed.append(t)

    analyzed.sort(key=lambda x: x["score"], reverse=True)

    return analyzed


# ============================================================
# 일정 설명 생성
# ============================================================

def build_reason(task):

    reasons = []

    if task["deadline"] <= 2:
        reasons.append("마감이 임박")

    if task["importance"] >= 4:
        reasons.append("중요도가 높음")

    if task["difficulty"] >= 4:
        reasons.append("난이도가 높음")

    if task["duration"] >= 3:
        reasons.append("긴 작업")

    if len(reasons) == 0:
        reasons.append("균형 배치")

    return ", ".join(reasons)


# ============================================================
# 발표용 Thinking Log
# ============================================================

def generate_reasoning(tasks):

    analyzed = analyze_tasks(tasks)

    logs = []

    for idx, task in enumerate(analyzed, start=1):

        logs.append({

            "rank": idx,

            "task": task["name"],

            "score": task["score"],

            "category": task["category"],

            "reason": build_reason(task)

        })

    return logs


# ============================================================
# Replan 여부 판단 (Fallback)
# ============================================================

def should_replan(stress_score):

    return stress_score >= 70


# ============================================================
# Replan 전략
# ============================================================

def suggest_strategy(stress_score):

    if stress_score >= 85:

        return {
            "action": "SPLIT",
            "message": "업무를 분할하고 휴식을 추가합니다."
        }

    elif stress_score >= 70:

        return {
            "action": "SHIFT",
            "message": "일부 업무를 다음 날로 이동합니다."
        }

    return {
        "action": "KEEP",
        "message": "현재 스케줄을 유지합니다."
    }


# ============================================================
# 발표용 AI 한 줄 설명
# ============================================================

def overall_comment(stress_score):

    if stress_score >= 85:
        return "AI가 과부하를 감지하여 재계획을 수행했습니다."

    elif stress_score >= 70:
        return "AI가 스트레스를 줄이기 위해 일부 일정을 조정했습니다."

    elif stress_score >= 45:
        return "AI가 균형 잡힌 일정으로 판단했습니다."

    return "AI가 매우 여유로운 일정으로 판단했습니다."