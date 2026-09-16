import streamlit as st
import openai

# 1. 페이지 설정 (기본 깔끔한 테마)
st.set_page_config(page_title="Clean AI Chatbot", layout="centered")

# 2. 사이드바 (API 키 및 모델 설정)
with st.sidebar:
    st.title("API 설정")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.markdown("[OpenAI API 키 발급받기](https://platform.openai.com/api-keys)")
    
    st.divider()
    
    selected_model = st.selectbox(
        "🤖 AI 모델 선택",
        ("gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo")
    )
    st.caption("API 키를 입력해야 대화가 가능합니다.")
    
    # 대화 기록 초기화 버튼
    if st.button("🗑️ 대화 기록 지우기"):
        st.session_state.messages = []
        st.rerun()

# 3. 메인 화면 헤더
st.title("💬 대화형 AI 챗봇")
st.caption("디자인 요소를 배제하고 대화 기억 기능과 안정성에 집중한 기본 버전입니다.")

# 4. 세션 상태(대화 기록) 초기화 및 저장
# 이 부분이 과거의 대화 내용을 기억하게 해주는 핵심 로직입니다.
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 기존 대화 기록을 화면에 순서대로 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 처리 및 API 호출
if prompt := st.chat_input("메시지를 입력하세요..."):
    # API 키 확인
    if not api_key:
        st.warning("👈 왼쪽 사이드바에 OpenAI API Key를 먼저 입력해주세요!")
        st.stop()

    # 사용자 메시지를 세션(기억)에 저장하고 화면에 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 7. OpenAI API 호출 (대화 기록 전체를 전달하여 문맥 기억)
    client = openai.OpenAI(api_key=api_key)
    
    with st.chat_message("assistant"):
        try:
            # st.session_state.messages 안에 있는 모든 이전 대화를 API로 보내어 기억을 유지합니다.
            stream = client.chat.completions.create(
                model=selected_model,
                messages=st.session_state.messages, 
                stream=True
            )
            
            # 스트리밍 출력 (타이핑 효과)
            response = st.write_stream(stream)
            
            # AI의 응답을 다시 세션(기억)에 저장
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")