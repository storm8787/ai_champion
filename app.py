import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI 챔피언 데모 앱")
st.write("Streamlit + Python 기본 기능 데모입니다.")

# -----------------------------------
# 1) 텍스트 요약(샘플, 실제 요약 아님)
# -----------------------------------
st.header("① 텍스트 요약 데모")

text_input = st.text_area("요약할 텍스트를 입력하세요:")

if st.button("요약하기"):
    if len(text_input.strip()) == 0:
        st.warning("텍스트를 입력해주세요.")
    else:
        # 아주 단순한 요약(앞부분 100자만 표시) - API 없이도 동작하도록 구성
        summary = text_input[:100] + "..."
        st.success("요약 결과:")
        st.write(summary)


# -----------------------------------
# 2) 파일 업로드 + 데이터 미리보기
# -----------------------------------
st.header("② 파일 업로드 / 데이터 확인")

uploaded = st.file_uploader("CSV 또는 XLSX 파일 업로드", type=["csv", "xlsx"])

if uploaded:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.subheader("데이터 미리보기")
    st.dataframe(df.head())


# -----------------------------------
# 3) 그래프 시각화 (matplotlib)
# -----------------------------------
st.header("③ 샘플 차트 시각화")

sample_data = pd.DataFrame({
    "월": [1, 2, 3, 4, 5, 6],
    "방문객 수": [1200, 1800, 900, 2200, 2600, 2000]
})

if st.button("그래프 그리기"):
    fig, ax = plt.subplots()
    ax.plot(sample_data["월"], sample_data["방문객 수"], marker='o')
    ax.set_title("월별 방문객 추이")
    ax.set_xlabel("월")
    ax.set_ylabel("방문객 수")
    st.pyplot(fig)

st.info("※ 이 예제는 Streamlit 기본 기능 테스트용입니다.")
