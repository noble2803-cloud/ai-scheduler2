import streamlit as st
import time


def show_reason():

    placeholder = st.empty()

    messages = [

        "회의가 많습니다.",

        "오전 집중시간을 확보합니다.",

        "빈 시간을 발견했습니다.",

        "휴식을 추가합니다.",

        "스트레스를 감소시킵니다."

    ]

    for msg in messages:

        placeholder.info(msg)

        time.sleep(0.8)

    placeholder.success("최적화 완료")