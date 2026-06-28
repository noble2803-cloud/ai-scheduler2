# ============================================================
# random_schedule.py (v4)
# 발표용 고정 일정 생성
# ============================================================

import random
from copy import deepcopy

# ============================================================
# 시간 유틸
# ============================================================

WORK_START = 9
WORK_END = 18

# ============================================================
# 기본 일정 Pool
# ============================================================

MORNING_EVENTS = [

    "출근",

    "메일 확인",

    "데일리 미팅",

    "업무 계획",

    "팀 브리핑"

]

AFTERNOON_EVENTS = [

    "점심",

    "회의",

    "자료 조사",

    "협업",

    "문서 작성"

]

EVENING_EVENTS = [

    "회의 정리",

    "메일 답변",

    "업무 마무리",

    "내일 계획"

]

BREAK_EVENTS = [

    "☕ 커피타임",

    "🍪 간식",

    "🚶 산책",

    "🧘 스트레칭"

]

# ============================================================
# 일정 추가
# ============================================================

def add_schedule(day_schedule, name, start, end, schedule_type):

    day_schedule.append({

        "task": name,

        "start": start,

        "end": end,

        "type": schedule_type

    })

# ============================================================
# 하루 일정 생성
# ============================================================

def generate_day():

    schedule = []

    # ---------------------------
    # 오전
    # ---------------------------

    add_schedule(

        schedule,

        random.choice(MORNING_EVENTS),

        9,

        10,

        "FIXED"

    )

    # ---------------------------
    # 오전 업무
    # ---------------------------

    if random.random() < 0.8:

        add_schedule(

            schedule,

            random.choice(MORNING_EVENTS),

            10,

            11,

            "FIXED"

        )

    # ---------------------------
    # 점심
    # ---------------------------

    add_schedule(

        schedule,

        "점심",

        12,

        13,

        "REST"

    )

    # ---------------------------
    # 오후
    # ---------------------------

    hour = 13

    while hour < 17:

        if random.random() < 0.75:

            add_schedule(

                schedule,

                random.choice(AFTERNOON_EVENTS),

                hour,

                hour + 1,

                "FIXED"

            )

        else:

            add_schedule(

                schedule,

                random.choice(BREAK_EVENTS),

                hour,

                hour + 1,

                "REST"

            )

        hour += 1

    # ---------------------------
    # 퇴근 전
    # ---------------------------

    if random.random() < 0.8:

        add_schedule(

            schedule,

            random.choice(EVENING_EVENTS),

            17,

            18,

            "FIXED"

        )

    schedule.sort(key=lambda x: x["start"])

    return schedule

# ============================================================
# 주간 일정 생성
# ============================================================

def generate_base_week():

    return {

        "Monday": generate_day(),

        "Tuesday": generate_day(),

        "Wednesday": generate_day(),

        "Thursday": generate_day(),

        "Friday": generate_day(),

        "Saturday": [],

        "Sunday": []

    }

# ============================================================
# 발표용 랜덤 변화
# ============================================================

def randomize_existing_schedule(week):

    week = deepcopy(week)

    for day in week:

        if len(week[day]) == 0:
            continue

        # 30% 확률로 휴식 추가
        if random.random() < 0.3:

            week[day].append({

                "task": random.choice(BREAK_EVENTS),

                "start": 15,

                "end": 16,

                "type": "REST"

            })

        # 20% 확률로 회의 추가
        if random.random() < 0.2:

            week[day].append({

                "task": "긴급 회의",

                "start": 16,

                "end": 17,

                "type": "FIXED"

            })

        week[day] = sorted(

            week[day],

            key=lambda x: x["start"]

        )

    return week

# ============================================================
# 발표용 한 줄 설명
# ============================================================

def explain_random_schedule():

    return (
        "기존 일정은 실제 사용자의 캘린더를 가정하여 "
        "AI가 빈 시간을 탐색한 뒤 새로운 업무를 자동 배치합니다."
    )