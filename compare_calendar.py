import pandas as pd
import streamlit as st


DAY_MAP = {
    "Monday": "월",
    "Tuesday": "화",
    "Wednesday": "수",
    "Thursday": "목",
    "Friday": "금"
}


def make_calendar(week):

    rows = []

    for h in range(9, 19):

        rows.append({

            "시간": f"{h:02d}:00",

            "월": "",

            "화": "",

            "수": "",

            "목": "",

            "금": ""

        })

    df = pd.DataFrame(rows)

    for day in week:

        if day not in DAY_MAP:
            continue

        col = DAY_MAP[day]

        for task in week[day]:

            hour = task["start"]

            if 9 <= hour <= 18:

                idx = hour - 9

                text = task["task"]

                if task.get("changed"):

                    text = "🟨 " + task["task"]

                elif task.get("added"):

                    text = "🟩 " + task["task"]

                else:

                    text = task["task"]

    return df


def compare_calendar(before, after):

    st.header("📊 Before vs After")

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("기존 일정")

        st.dataframe(

            make_calendar(before),

            hide_index=True,

            use_container_width=True

        )

    with c2:

        st.subheader("AI 최적화")

        st.dataframe(

            make_calendar(after),

            hide_index=True,

            use_container_width=True

        )

    st.info("🟨 : AI가 새롭게 추가한 일정")
