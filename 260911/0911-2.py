import streamlit as st
import openai

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="Dream Glass AI", initial_sidebar_state="expanded")

# 2. 글로벌 CSS
st.markdown("""
<style>
    /* 상단바 투명화 */
    header { background-color: transparent !important; }
    
    /* 사이드바 아이콘 완벽 숨김 및 이모지 교체 */
    [data-testid="collapsedControl"] * { display: none !important; }
    [data-testid="collapsedControl"]::after {
        content: "👉"; font-size: 1.4rem; display: block; text-align: center;
    }
    
    /* 사이드바 버튼 글래스모피즘 효과 */
    [data-testid="collapsedControl"] {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(12px) !important; border-radius: 50% !important;
        box-shadow: 0 4px 15px rgba(31, 38, 135, 0.15) !important;
        margin: 15px !important; width: 45px !important; height: 45px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        transition: all 0.2s;
    }
    [data-testid="collapsedControl"]:hover { background: rgba(255, 255, 255, 0.6) !important; transform: scale(1.1); }
    
    /* 구름 애니메이션 */
    @keyframes cloudDrift {
        0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; }
    }

    /* 몽환적인 파스텔 구름 배경 */
    .stApp {
        background-color: #a1c4fd;
        background-image: url('https://images.unsplash.com/photo-1509803874385-db7c23652552?q=80&w=2000&auto=format&fit=crop');
        background-size: 150% 150%; background-attachment: fixed; animation: cloudDrift 120s ease-in-out infinite; 
    }
    
    /* 메인 화면 중앙 정렬 및 박스 깨짐 방지 */
    .block-container {
        max-width: 900px !important; margin: 0 auto;
        padding-top: 3rem !important; padding-bottom: 12rem !important;
        box-sizing: border-box !important;
    }

    /* 챗봇 초기 웰컴 카드 */
    .welcome-card {
        background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 36px; padding: 4rem 3rem; text-align: center;
        margin-top: 8vh; box-shadow: 0 10px 40px rgba(31, 38, 135, 0.15); color: #1e293b;
        font-weight: 600 !important; animation: fadeIn 0.8s ease-out; box-sizing: border-box !important;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    /* 🚨 1. 말풍선 캡슐 스타일 (글자 깨짐 및 삐져나옴 완벽 방지) */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.3) !important; backdrop-filter: blur(16px) !important; -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important; border-radius: 28px !important; padding: 2rem 2.5rem !important;
        margin-bottom: 1.5rem !important; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        box-sizing: border-box !important;
        word-break: break-word !important; /* 긴 텍스트 강제 줄바꿈 */
        overflow-wrap: break-word !important;
    }
    
    /* 말풍선 내부 텍스트 폰트 설정 */
    [data-testid="stChatMessage"] p {
        color: #1e293b !important; font-size: 1.15rem !important;
        font-weight: 600 !important; line-height: 1.7 !important; margin: 0 !important;
    }

    [data-testid="stChatMessageAvatarIcon"] {
        background-color: rgba(255, 255, 255, 0.6) !important; width: 3.5rem !important; height: 3.5rem !important;
    }

    /* 하단 입력창 플로팅 캡슐 형태 */
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important; position: fixed !important; bottom: 2.5rem !important;
        left: 50% !important; transform: translateX(-50%) !important; width: 100% !important; max-width: 900px !important;
        padding: 0 1.5rem !important; z-index: 999; box-sizing: border-box !important;
    }

    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.4) !important; backdrop-filter: blur(24px) !important; -webkit-backdrop-filter: blur(24px) !important;
        border: 2px solid rgba(255, 255, 255, 0.8) !important; border-radius: 40px !important; box-shadow: 0 15px 35px rgba(31, 38, 135, 0.2) !important;
        box-sizing: border-box !important;
    }

    [data-testid="stChatInputTextArea"] {
        color: #0f172a !important; font-size: 1.25rem !important; font-weight: 600 !important; padding: 1.2rem 1.5rem !important;
    }
    
    [data-testid="stChatInputTextArea"]::placeholder {
        color: #64748b !important; font-weight: 500 !important;
    }

    [data-testid="stChatInputSubmitButton"] {
        color: #0284c7 !important; transform: scale(1.3); margin-right: 15px;
    }

    /* 사이드바 글래스모피즘 */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.25) !important; backdrop-filter: blur(24px) !important; -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.4) !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        font-size: 1.15rem !important; font-weight: 600 !important; color: #0f172a !important;
    }

    /* API 가져오기 버튼 */
    .api-link-btn {
        display: block; text-align: center; background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.8); border-radius: 12px; padding: 12px; margin-top: -10px; margin-bottom: 20px;
        color: #0f172a !important; text-decoration: none; font-weight: 800 !important; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(31, 38, 135, 0.1); transition: all 0.2s;
    }
    .api-link-btn:hover { background: rgba(255, 255, 255, 0.6); transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# 3. 사이드바 설정
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.markdown('<a href="https://platform.openai.com/api-keys" target="_blank" class="api-link-btn">🔑 OpenAI API 가져오기</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 🤖 Model Selection")
    selected_model = st.selectbox("사용할 모델 지정:", ("gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"), index=0)
    
    st.success(f"**현재 활성화된 모델:**\n\n✨ {selected_model}")
    st.markdown("---")
    st.caption("※ API 키를 입력한 후, 하단 중앙의 채팅창에서 대화를 시작하세요!")

# 4. 세션 상태(대화 기록) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 대화 기록이 없을 때 나타나는 봇 웰컴 카드
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-card">
            <div style="font-size: 4rem; margin-bottom: 10px;">☁️</div>
            <h1 style="font-size: 2.2rem; margin-bottom: 15px;">Dream Glass AI</h1>
            <p style="font-size: 1.3rem; line-height: 1.6;">
                반갑습니다! 왼쪽 사이드바에 OpenAI API 키를 입력하고<br>
                하단의 캡슐 입력창에서 자유롭게 대화를 시작해보세요.
            </p>
        </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. 사용자 입력 처리
if prompt := st.chat_input("무엇이든 물어보세요..."):
    if not api_key:
        st.warning("👈 왼쪽 사이드바에 OpenAI API Key를 먼저 입력해주세요!")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# 7. 🚨 2. OpenAI 통신 강화 및 스트리밍 처리 로직
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    client = openai.OpenAI(api_key=api_key)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            
            # 구버전/신버전 라이브러리 호환을 위한 안전한 제너레이터 함수
            def generate_response():
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content

            response = st.write_stream(generate_response())
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"오류가 발생했습니다 (API Key가 정확한지 확인해주세요): {e}")