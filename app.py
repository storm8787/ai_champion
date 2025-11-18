import os
import platform
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from openai import OpenAI

# =========================
# 0. OpenAI 클라이언트 설정
# =========================
# Streamlit Cloud의 Secrets에 다음과 같이 저장해 둬야 함:
# OPENAI_API_KEY = "sk-xxxx..."
api_key = st.secrets.get("OPENAI_API_KEY", None)

if api_key is None:
    st.error("❌ OPENAI_API_KEY가 설정되어 있지 않습니다. Streamlit Cloud Secrets를 확인해주세요.")
else:
    client = OpenAI(api_key=api_key)

# =========================
# 1. 한글 폰트 설정 함수
# =========================
def set_korean_font():
    """
    - Windows: 맑은 고딕
    - 로컬/Cloud에서 NanumGothic.ttf가 있으면 그 폰트 사용
    - 그 외: DejaVu Sans(기본 폰트)로 fallback
    """
    try:
        # 1) 우선 레포 안에 NanumGothic.ttf 있는지 확인
        font_path = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
        if os.path.exists(font_path):
            font_manager.fontManager.addfont(font_path)
            font_name = font_manager.FontProperties(fname=font_path).get_name()
            rcParams["font.family"] = font_name
        else:
            # 2) NanumGothic이 없으면 OS별 기본값
            system = platform.system()
            if system == "Windows":
                rcParams["font.family"] = "Malgun Gothic"
            elif system == "Darwin":  # macOS
                rcParams["font.family"] = "AppleGothic"
            else:
                # 리눅스 계열: 기본 DejaVu Sans로 시도
                rcParams["font.family"] = "DejaVu Sans"

        # 마이너스 기호 깨짐 방지
        rcParams["axes.unicode_minus"] = False
    except Exception as e:
        st.warning(f"폰트 설정 중 오류가 발생했습니다: {e}")
        # 폰트 설정 실패해도 앱이 죽지 않도록 기본값 유지


set_korean_font()

# =========================
# 2. Streamlit UI 시작
# =========================
st.title("AI 챔피언 사전 점검용 앱 💻")
st.write("OpenAI API 연결 상태와 한글 그래프 표시 상태를 동시에 점검하는 테스트 앱입니다.")

# ------------------------------------
# 2-1. OpenAI Q&A 테스트
# ------------------------------------
st.header("① OpenAI Q&A 테스트")

user_question = st.text_area(
    "질문을 입력하세요.",
    placeholder="예) 행정업무 자동화 아이디어를 3가지만 간단히 설명해줘.",
    height=120,
)

if st.button("질문 보내기"):
    if api_key is None:
        st.error("OPENAI_API_KEY가 설정되어 있지 않아 API를 호출할 수 없습니다.")
    elif not user_question.strip():
        st.warning("질문을 입력해주세요.")
    else:
        with st.spinner("GPT가 답변을 생성 중입니다..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "너는 대한민국 지방자치단체 공무원의 업무를 돕는 한국어 비서이다. "
                                "질문에 대해 친절하고 간결하게, 이해하기 쉽게 설명한다."
                            ),
                        },
                        {
                            "role": "user",
                            "content": user_question,
                        },
                    ],
                )
                answer = response.choices[0].message.content
                st.success("✅ API 호출 성공")
                st.markdown("**답변:**")
                st.write(answer)
            except Exception as e:
                st.error("❌ API 호출 중 오류가 발생했습니다.")
                st.code(str(e))


# ------------------------------------
# 2-2. 한글 그래프 깨짐 테스트
# ------------------------------------
st.header("② 한글 그래프 표시 테스트")

sample_data = pd.DataFrame(
    {
        "월": [1, 2, 3, 4, 5, 6],
        "방문객 수": [1200, 1800, 900, 2200, 2600, 2000],
    }
)

if st.button("한글 그래프 그리기"):
    fig, ax = plt.subplots()
    ax.plot(sample_data["월"], sample_data["방문객 수"], marker="o")
    ax.set_title("월별 방문객 추이 (한글 폰트 테스트)")
    ax.set_xlabel("월")
    ax.set_ylabel("방문객 수(명)")
    st.pyplot(fig)

st.info("※ NanumGothic.ttf 파일을 레포 최상위에 넣어두면, Streamlit Cloud에서도 한글이 훨씬 안정적으로 표시됩니다.")
