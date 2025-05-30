import streamlit as st
import google.generativeai as genai
from typing import List, Dict

# 페이지 설정
st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="🤖",
    layout="wide"
)

# Gemini API 설정
def configure_genai():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API 키 설정 중 오류가 발생했습니다: {str(e)}")
        return None

# 대화 기록 초기화
def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# 메시지 표시 함수
def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 메인 애플리케이션
def main():
    st.title("🤖 Gemini 챗봇")
    
    # Gemini 모델 초기화
    model = configure_genai()
    if not model:
        st.stop()
    
    # 채팅 기록 초기화
    initialize_chat_history()
    
    # 채팅 인터페이스
    display_messages()
    
    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("생각 중..."):
                try:
                    # 대화 컨텍스트 생성
                    chat = model.start_chat(history=[])
                    response = chat.send_message(prompt)
                    
                    # 응답 표시 및 저장
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"응답 생성 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
