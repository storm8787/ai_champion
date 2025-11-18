import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from openai import OpenAI

# ------------------------------------
# 0. OpenAI 클라이언트 설정 (Streamlit Cloud Secrets 사용)
# ------------------------------------
# Streamlit Cloud의 Secrets에 OPENAI_API_KEY 넣어두고 사용:
# OPENAI_API_KEY = "sk-xxxx..."
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.title("AI 챔피언 테스트 앱 🧪")

# ------------------------------------
# 1. OpenAI API 연결 테스트
# ------------------------------------
st.header("① OpenAI API 연결 상태 테스트")

if st.button("API 호출해보기"):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 사용하는 모델명
            messages=[
                {"role": "system", "content": "너는 간단히만 대답하는 한국어 비서야."},
                {"role": "user", "content": "지금 이 메시지가 보인다면 API 연결이 잘 된 거야. 한 줄로 짧게 대답해줘."}
            ],
        )
        answer = response.choices[0].message.content
        st.success("✅ API 호출 성공!")
        st.write(answer)
    except Exception as e:
        st.error("❌ API 호출 중 오류가 발생했습니다.")
        st.code(str(e))


# ------------------------------------
# 2. 한글 안 깨지는 그래프 테스트
# ------------------------------------
st.header("② 한글 그래프 표시 테스트")

# 🔧 한글 폰트 설정
# - Windows: 'Malgun Gothic'
# - macOS: 'AppleGothic'
# - 리눅스/Cloud: 'NanumGothic' 폰트 추가해두면 좋음
plt.rcParams["font.family"] = ["Malgun Gothic", "AppleGothic", "NanumGothic", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지

data = pd.DataFrame({
    "월": [1, 2, 3, 4, 5, 6],
    "방문객 수": [1200, 1800, 900, 2200, 2600, 2000]
})

if st.button("한글 그래프 그리기"):
    fig, ax = plt.subplots()
    ax.plot(data["월"], data["방문객 수"], marker="o")
    ax.set_title("월별 방문객 추이 (테스트)")
    ax.set_xlabel("월")
    ax.set_ylabel("방문객 수(명)")
    st.pyplot(fig)

st.info("※ 이 앱은 OpenAI API 연결 및 한글 그래프 표시 테스트용입니다.")
