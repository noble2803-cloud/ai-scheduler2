import streamlit as st


def analyze_changes(before, after):

    changes = []

    for day in before:

        before_tasks = {}

        after_tasks = {}

        for task in before[day]:

            before_tasks[task["task"]] = task["start"]

        for task in after[day]:

            after_tasks[task["task"]] = task["start"]

        # 새 일정
        for task in after_tasks:

            if task not in before_tasks:

                changes.append({
                    "type": "ADD",
                    "text": f"'{task}' 일정이 새로 추가되었습니다."
                })

        # 삭제
        for task in before_tasks:

            if task not in after_tasks:

                changes.append({
                    "type": "DELETE",
                    "text": f"'{task}' 일정이 제거되었습니다."
                })

        # 시간 변경
        for task in before_tasks:

            if task in after_tasks:

                if before_tasks[task] != after_tasks[task]:

                    changes.append({

                        "type": "MOVE",

                        "text":

                        f"'{task}' 시간이 "

                        f"{before_tasks[task]}시 → "

                        f"{after_tasks[task]}시로 변경되었습니다."

                    })

    return changes


def show_changes(changes):

    st.header("🤖 AI 변경 사항")

    if len(changes) == 0:

        st.success("변경된 일정이 없습니다.")

        return

    for c in changes:

        if c["type"] == "ADD":

            st.success("➕ " + c["text"])

        elif c["type"] == "MOVE":

            st.warning("🔄 " + c["text"])

        elif c["type"] == "DELETE":

            st.error("➖ " + c["text"])