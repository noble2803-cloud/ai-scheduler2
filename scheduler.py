# ============================================================
# scheduler.py (v4)
# AI Scheduler Agent Core
# ============================================================

from copy import deepcopy
import random

# ============================================================
# 기본 설정
# ============================================================

WORK_START = 9
WORK_END = 18

MAX_REPLAN = 2
STRESS_THRESHOLD = 70

# ============================================================
# Priority Score
# ============================================================

def calculate_priority(task):

    urgency = (8 - task["deadline"]) * 15
    importance = task["importance"] * 12
    difficulty = task["difficulty"] * 8
    duration = task["duration"] * 4

    return urgency + importance + difficulty + duration

# ============================================================
# 빈 시간 찾기
# ============================================================

def find_slot(schedule, duration):

    schedule = sorted(schedule, key=lambda x: x["start"])

    current = WORK_START

    for item in schedule:

        if item["start"] - current >= duration+1:
            return current

        current = max(current, item["end"])

    if WORK_END - current >= duration+1:
        return current

    return None

# ============================================================
# 일정 추가
# ============================================================
def add_buffer(day_schedule):

    if random.random() < 0.3:

        slot = find_slot(day_schedule, 1)

        if slot is not None:

            day_schedule.append({

                "task": "🧘 여유시간",

                "start": slot,

                "end": slot + 1,

                "type": "BUFFER"

            })


def place_task(day_schedule, task):

    slot = find_slot(day_schedule, task["duration"])

    if slot is None:
        return False

    day_schedule.append({

        "task": task["name"],
        "start": slot,
        "end": slot + task["duration"],
        "type": "AI",
        "added":True,
        "changed":False,
        "fixed": task.get("fixed", False)

    })

    return True

# ============================================================
# 휴식 추가
# ============================================================

def insert_rest(day_schedule):

    if random.random() < 0.6:

        slot = find_slot(day_schedule, 1)

        if slot is not None:

            day_schedule.append({

                "task": random.choice([
                    "☕ 커피타임",
                    "🚶 산책",
                    "🧘 스트레칭",
                    "🍪 간식"
                ]),

                "start": slot,
                "end": slot + 1,
                "type": "REST"

            })

# ============================================================
# 기본 스케줄 생성
# ============================================================

def optimize_schedule(tasks, week):

    week = deepcopy(week)

    logs = []

    sorted_tasks = sorted(
        tasks,
        key=calculate_priority,
        reverse=True
    )

    for task in sorted_tasks:

        best_day = None

        for day in week.keys():

            temp = deepcopy(week[day])

            if place_task(temp, task):

                week[day] = temp

                best_day = day

                break

        if best_day:

            logs.append({

                "task": task["name"],
                "day": best_day,
                "priority": calculate_priority(task)

            })

    return week, logs



# ============================================================
# Task 재정렬
# ============================================================

def reprioritize(tasks):

    new_tasks = deepcopy(tasks)

    for task in new_tasks:

        if task["difficulty"] >= 4:

            task["deadline"] += 1

    return sorted(
        new_tasks,
        key=calculate_priority,
        reverse=True
    )

# ============================================================
# 스케줄 흔들기
# ============================================================

def perturb_schedule(week):

    week = deepcopy(week)

    days = list(week.keys())

    if len(days) < 2:
        return week

    source = random.choice(days)
    target = random.choice(days)

    if source == target:
        return week

    if len(week[source]) == 0:
        return week

    moved = week[source].pop()
    
    movable = [

        t

        for t in week[source]
        if not t.get("fixed", False)
    ]
    if len(movable) == 0:
        return week

    moved = random.choice(movable)
    week[source].remove(moved)

    moved["changed"] = True
    week[target].append(moved)

    return week

# ============================================================
# Agent Loop
# ============================================================

def agent_optimize(

    tasks,
    base_week,
    reflect_fn,
    replan_fn

):

    week = deepcopy(base_week)

    history = []

    logs = []

    for round_idx in range(MAX_REPLAN):

        week, logs = optimize_schedule(tasks, week)

        stress = reflect_fn(week)

        need_replan = replan_fn(stress)

        history.append({

            "round": round_idx + 1,

            "stress": stress,

            "replan": need_replan

        })

        if not need_replan:

            break

        tasks = reprioritize(tasks)

        week = perturb_schedule(week)

    # 휴식 자동 삽입
    for day in week:

        insert_rest(week[day])

    return week, logs, history

# ============================================================
# 발표용 Thinking Log
# ============================================================

def generate_thinking(logs):

    thinking = []

    for log in logs:

        thinking.append(

            f"{log['task']}의 우선순위({log['priority']})가 높아 "
            f"{log['day']}에 우선 배치했습니다."

        )

    return thinking
