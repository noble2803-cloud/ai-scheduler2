import pandas as pd
import streamlit as st


def draw_calendar(week, daily=None):

    hours = list(range(9, 19))

    columns = [
        "시간",
        "월\n(Stress)",
        "화\n(Stress)",
        "수\n(Stress)",
        "목\n(Stress)",
        "금\n(Stress)"
    ]

    rows = []

    day_map = {

        "Monday": "월",

        "Tuesday": "화",

        "Wednesday": "수",

        "Thursday": "목",

        "Friday": "금"

    }

    for h in hours:

        row = {

            "시간": f"{h:02d}:00"

        }

        for d in ["월", "화", "수", "목", "금"]:

            row[d] = ""

        rows.append(row)

    df = pd.DataFrame(rows)

    if daily:
        stress_row = {
            "시간":"🔥 Stress"
        }
        reverse = {
            "Monday":"월",
            "Tuesday":"화",
            "Wednesday":"수",    
            "Thursday":"목",    
            "Friday":"금"
        }

        for eng, kor in reverse.items():
            if eng in daily:
                stress_row[kor] = daily[eng]["score"]
            else:
                stress_row[kor] = "-"
        df = pd.concat(
            [
                pd.DataFrame([stress_row]),
                df
            ],
            ignore_index=True
        )

    
    for day in week:

        if day not in day_map:

            continue

        col = day_map[day]

        for task in week[day]:

            hour = task["start"]

            idx = hour - 9

            if 0 <= idx < len(df):

                df.loc[idx, col] = task["task"]

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )
