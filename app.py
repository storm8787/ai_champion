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
