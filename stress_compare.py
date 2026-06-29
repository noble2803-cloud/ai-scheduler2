import streamlit as st


def draw_stress_compare(before_score, after_score):

    st.header("🧠 Stress Improvement")

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("Before")

        st.metric(

            "Stress",

            f"{before_score:.1f}"

        )

        st.progress(min(before_score / 100, 1.0))

    with c2:

        st.subheader("After")

        delta = after_score - before_score

        st.metric(

            "Stress",

            f"{after_score:.1f}",

            delta=f"{delta:.1f}"

        )

        st.progress(min(after_score / 100, 1.0))

    improvement = before_score - after_score

    if improvement > 0:

        st.success(

            f"✅ AI가 스트레스를 {improvement:.1f}점 감소시켰습니다."

        )

    elif improvement == 0:

        st.info("변화 없음")

    else:

        st.error(

            f"⚠ 스트레스가 {-improvement:.1f}점 증가했습니다."
        )