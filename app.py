import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 OPENAI_API_KEY (및 선택적으로 OPENAI_MODEL) 읽기
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

LANGUAGES = {
    "영어 (English)": "English",
    "스페인어 (Español)": "Spanish",
    "베트남어 (Tiếng Việt)": "Vietnamese",
}


def translate(client: OpenAI, text: str, target_language: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a professional translator. Translate the user's text into {target_language}. "
                    "Output only the translated text, without explanations or quotes."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


st.set_page_config(page_title="번역기", page_icon="🌐")
st.title("🌐 간단 번역기")
st.caption(f"OpenAI `{MODEL}` 모델을 사용합니다.")

if not API_KEY:
    st.error(".env 파일에 OPENAI_API_KEY 가 설정되어 있지 않습니다.")
    st.stop()

client = OpenAI(api_key=API_KEY)

text = st.text_area("번역할 글을 입력하세요", height=200)
language_label = st.radio("번역할 언어를 선택하세요", list(LANGUAGES.keys()), horizontal=True)

if st.button("번역하기", type="primary"):
    if not text.strip():
        st.warning("번역할 글을 입력해주세요.")
    else:
        with st.spinner("번역 중..."):
            try:
                result = translate(client, text, LANGUAGES[language_label])
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {e}")
            else:
                st.subheader(f"번역 결과 — {language_label}")
                st.text_area("결과", result, height=200, label_visibility="collapsed")
