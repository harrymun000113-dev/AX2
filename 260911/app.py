
import streamlit as st
import openai

# 1. 페이지 설정 (중앙 집중형 레이아웃을 위해 wide로 두고 CSS로 너비를 제한합니다)
st.set_page_config(layout="wide", page_title="Dream Glass AI", initial_sidebar_state="expanded")

# 2. 글로벌 CSS: 동글동글한 폰트, 큼직한 UI, 챗봇 중앙 정렬, API 링크 버튼 스타일
st.markdown("""
<style>
    /* 동글동글하고 깔끔한 나눔스퀘어라운드 폰트 렌더링 */
    @font-face {
        font-family: 'NanumSquareRound';
        src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_twelve@1.1/NanumSquareRound.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }
    
    * { font-family: 'NanumSquareRound', sans-serif !important; }

    /* 상단바 투명화 (사이드바 여닫기 버튼 보존) */
    header { background-color: transparent !important; }
    
    /* 몽환적인 파스텔 구름 배경 (스크롤 고정) */
    .stApp {
        background-color: #a1c4fd;
        background-image: url('https://images.unsplash.com/photo-1509803874385-db7c23652552?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* 메인 화면 중앙 정렬 및 너비 제한 (UX 깔끔하게) */
    .block-container {
        max-width: 900px !important;
        margin: 0 auto;
        padding-top: 3rem !important;
        padding-bottom: 12rem !important; /* 하단 플로팅 입력창에 가려지지 않도록 넉넉히 여백 */
    }

    /* 챗봇 초기 웰컴 카드 (아무 대화 없을 때 중앙에 표시) */
    .welcome-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 36px;
        padding: 4rem 3rem;
        text-align: center;
        margin-top: 8vh;
        box-shadow: 0 10px 40px rgba(31, 38, 135, 0.15);
        color: #1e293b;
        animation: fadeIn 0.8s ease-out;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    /* 말풍선 스타일 및 크기 확대 */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        border-radius: 28px !important;
        padding: 2rem 2.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        color: #1e293b !important;
        font-size: 1.3rem !important;
        line-height: 1.7 !important;
    }

    /* 프로필 아이콘 */
    [data-testid="stChatMessageAvatarIcon"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        width: 3.5rem !important;
        height: 3.5rem !important;
    }

    /* 하단 입력창을 바닥에서 띄워 중앙(플로팅) 캡슐 형태로 배치 */
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
        position: fixed !important;
        bottom: 2.5rem !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 900px !important;
        padding: 0 1.5rem !important;
        z-index: 999;
    }

    /* 실제 채팅 입력창 유리 질감 및 크기 */
    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 2px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 40px !important;
        box-shadow: 0 15px 35px rgba(31, 38, 135, 0.2) !important;
    }

    [data-testid="stChatInputTextArea"] {
        color: #0f172a !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        padding: 1.2rem 1.5rem !important;
    }
    
    [data-testid="stChatInputTextArea"]::placeholder {
        color: #64748b !important;
    }

    /* 전송 버튼 아이콘 */
    [data-testid="stChatInputSubmitButton"] {
        color: #0284c7 !important;
        transform: scale(1.3); 
        margin-right: 15px;
    }

    /* 사이드바 글래스모피즘 및 글자 크기 큼직하게 변경 */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.25) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.4) !important;
    }
    
    [data-testid="stSidebar"] * {
        font-size: 1.2rem !important;
        color: #0f172a !important;
    }

    /* 💡 API 가져오기 버튼 (글래스모피즘 커스텀) */
    .api-link-btn {
        display: block;
        text-align: center;
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 12px;
        margin-top: -10px;
        margin-bottom: 20px;
        color: #0f172a !important;
        text-decoration: none;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(31, 38, 135, 0.1);
        transition: all 0.2s;
    }
    .api-link-btn:hover {
        background: rgba(255, 255, 255, 0.6);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# 3. 사이드바 설정 (API 키 및 드롭다운 모델 선택)
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    # API 가져오기 버튼 (클릭 시 새 창으로 OpenAI 사이트 열림)
    st.markdown('<a href="https://platform.openai.com/api-keys" target="_blank" class="api-link-btn">🔑 OpenAI API 가져오기</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 🤖 Model Selection")
    
    # 모델 선택 드롭다운
    selected_model = st.selectbox(
        "사용할 모델 지정:",
        ("gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"),
        index=0
    )
    
    # 선택된 모델 시각적 강조
    st.success(f"**현재 활성화된 모델:**\n\n✨ {selected_model}")
    st.markdown("---")
    st.caption("사이드바에 API 키를 입력하면 즉시 대화가 활성화됩니다.")

# 4. 세션 상태(대화 기록) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 대화 기록이 없을 때 나타나는 봇 웰컴 카드 (화면 중앙)
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-card">
            <div style="font-size: 4rem; margin-bottom: 10px;">☁️</div>
            <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 15px;">Dream Glass AI</h1>
            <p style="font-size: 1.3rem; line-height: 1.6; font-weight: 600;">
                반갑습니다! 사이드바에 OpenAI API 키를 입력하시고<br>
                하단의 캡슐 입력창에서 자유롭게 대화를 시작해보세요.
            </p>
        </div>
    """, unsafe_allow_html=True)

# 6. 기존 대화 기록 화면에 렌더링
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. 사용자 입력 처리 및 OpenAI API 호출 (중앙 플로팅 입력창)
if prompt := st.chat_input("무엇이든 물어보세요..."):
    # API 키가 없는 경우 경고창 띄우고 중단
    if not api_key:
        st.warning("👈 왼쪽 사이드바에 OpenAI API Key를 먼저 입력해주세요!")
        st.stop()
        
    # 사용자 메시지 화면에 출력 및 기록
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 화면 강제 리렌더링으로 웰컴 카드를 지우고 메시지 출력
    st.rerun()

# 8. 챗봇 응답 처리 로직
# 리런(rerun) 이후 가장 마지막 메시지가 유저일 경우 봇이 대답하도록 설정
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    client = openai.OpenAI(api_key=api_key)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            # 스트리밍 응답 렌더링
            response = st.write_stream(stream)
            # 대화 기록에 챗봇 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")