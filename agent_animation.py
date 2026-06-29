import streamlit as st
import time


def run_agent_animation():

    status = st.empty()

    progress = st.progress(0)

    steps = [

        ("📅 기존 일정 분석",15),

        ("📊 업무량 계산",30),

        ("🔥 스트레스 예측",45),

        ("🔍 빈 시간 탐색",60),

        ("⚖️ 우선순위 계산",75),

        ("🤖 AI 일정 재배치",90),

        ("✅ 최적 일정 생성 완료",100)

    ]

    for text,value in steps:

        status.info(text)

        progress.progress(value)

        time.sleep(0.5)

    status.success("AI Agent가 최적 일정을 생성했습니다.")