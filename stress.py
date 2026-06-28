# ============================================================
# stress.py (v4)
# AI Scheduler Agent - Stress Analyzer
# ============================================================

from collections import defaultdict

# ============================================================
# Week → Flat List
# ============================================================

def flatten_week(week):

    items = []

    for day in week:

        for task in week[day]:

            new_task = task.copy()
            new_task["day"] = day
            items.append(new_task)

    return items


# ============================================================
# 하루 스트레스 계산
# ============================================================

def calculate_day_stress(tasks):

    if len(tasks) == 0:
        return {
            "score": 10,
            "level": "매우 여유",
            "message": "오늘은 여유로운 하루입니다 😊"
        }

    score = 0

    # 정렬
    tasks = sorted(tasks, key=lambda x: x["start"])

    previous_end = None
    consecutive = 0

    for task in tasks:

        duration = task["end"] - task["start"]

        # ------------------------------------------------
        # 휴식은 스트레스 감소
        # ------------------------------------------------

        if task["type"] == "REST":

            score -= 8
            consecutive = 0
            previous_end = task["end"]
            continue

        # ------------------------------------------------
        # 기본 업무
        # ------------------------------------------------

        score += duration * 10

        # ------------------------------------------------
        # 늦은 업무
        # ------------------------------------------------

        if task["end"] >= 17:
            score += 8

        # ------------------------------------------------
        # 오전 집중업무
        # ------------------------------------------------

        if task["start"] <= 10:
            score += 5

        # ------------------------------------------------
        # 연속업무
        # ------------------------------------------------

        if previous_end is not None:

            if task["start"] == previous_end:

                consecutive += 1

                score += consecutive * 5

            else:

                consecutive = 0

        previous_end = task["end"]

    score = max(0, min(score, 100))

    # ------------------------------------------------
    # Level
    # ------------------------------------------------

    if score >= 85:

        level = "매우 높음"

        message = "🔥 휴식이 꼭 필요합니다."

    elif score >= 70:

        level = "높음"

        message = "☕ 중간 휴식을 권장합니다."

    elif score >= 45:

        level = "보통"

        message = "🙂 무난한 일정입니다."

    else:

        level = "낮음"

        message = "😌 여유로운 하루입니다."

    return {

        "score": score,

        "level": level,

        "message": message

    }


# ============================================================
# 주간 분석
# ============================================================

def analyze_schedule(flat_items):

    day_dict = defaultdict(list)

    for item in flat_items:

        day = item.get("day", "Monday")

        day_dict[day].append(item)

    daily = {}

    total = 0

    for day in day_dict:

        result = calculate_day_stress(day_dict[day])

        daily[day] = result

        total += result["score"]

    if len(daily) == 0:

        average = 0

    else:

        average = round(total / len(daily), 1)

    return {

        "score": average,

        "daily": daily

    }


# ============================================================
# 발표용 추천
# ============================================================

def recommend_break(score):

    if score >= 85:

        return [

            "🚶 10분 산책",

            "🧘 스트레칭",

            "🥤 물 한 잔",

            "☕ 커피타임"

        ]

    elif score >= 70:

        return [

            "☕ 커피 한 잔",

            "🍪 간식",

            "🌿 창밖 보기"

        ]

    elif score >= 45:

        return [

            "🙂 가벼운 휴식"

        ]

    else:

        return [

            "👍 현재 페이스 유지"

        ]


# ============================================================
# 발표용 하루 요약
# ============================================================

def summary_text(result):

    score = result.get("score",0)

    if score>=85:
        level="매우 높음"
    elif score>=70:
        level="높음"
    elif score>=45:
        level="보통"
    else:
        level="낮음"

    return f"예상 스트레스는 {score}점이며 위험도는 '{level}' 입니다."
