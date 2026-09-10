import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="무역 직무 MBTI 테스트 | 취업 준비생 맞춤",
    page_icon="💼",
    layout="centered"
)

# 짙은 초록색/연두색 테마 + 친근하고 세련된 UI를 위한 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 앱 배경 및 폰트 */
    .stApp {
        background-color: #F0F7F4;
        color: #11261B;
    }
    
    /* 헤더 스타일 */
    h1, h2, h3 {
        color: #1B4332 !important;
        font-family: 'Malgun Gothic', sans-serif;
    }
    
    /* 서브 텍스트 카드 */
    .intro-box {
        background-color: #E8F5E9;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 6px solid #2D6A4F;
        margin-bottom: 2rem;
        font-size: 1.05rem;
        color: #1B4332;
    }

    /* 버튼 스타일 */
    .stButton>button {
        background-color: #2D6A4F;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        border: none;
        font-weight: bold;
        font-size: 1.05rem;
        box-shadow: 0 4px 6px rgba(45, 106, 79, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #40916C;
        color: white;
        box-shadow: 0 6px 8px rgba(45, 106, 79, 0.3);
    }
    
    /* 질문 카드 스타일 */
    .question-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #D8F3DC;
    }

    /* 결과 박스 스타일 */
    .result-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #D8F3DC 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid #52B788;
        text-align: center;
        color: #081C15;
        box-shadow: 0 10px 20px rgba(82, 183, 136, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# 타이틀 및 인트로
st.title("💼 무역 직무 성향 MBTI 테스트")
st.markdown("""
    <div class="intro-box">
        👋 안녕, 예비 무역인! 막막한 직무 선택 때문에 고민이지?<br>
        나의 성향과 평소 일하는 스타일을 바탕으로 <b>가장 잘 맞는 무역·해외사업 핵심 직무</b>를 찾아줄게. 
        편하게 마음 끌리는 선택지를 골라봐! 🚀
    </div>
""", unsafe_allow_html=True)

# 6개의 무역 관련 직무 정의 (취업준비생 맞춤 설명 및 강점 추가)
JOBS = {
    "해외영업": {
        "desc": "글로벌 바이어를 발굴하고 설득하여 수출 계약을 이끌어내는 무역의 최전방 개척자!",
        "strength": "협상력, 외국어 활용 능력, 적극적인 소통, 추진력",
        "trait": "외향적(E), 직관적(N), 사고형(T), 인식형(P)"
    },
    "무역물류관리": {
        "desc": "선적부터 창고 입고, 납기 준수까지 복잡한 글로벌 공급망의 흐름을 빈틈없이 통제하는 실무 마스터!",
        "strength": "꼼꼼함, 일정 관리 능력, 돌발 상황 대처 능력, 책임감",
        "trait": "내향적(I), 감각적(S), 사고형(T), 판단형(J)"
    },
    "해외마케팅": {
        "desc": "현지 시장 트렌드를 분석하고 글로벌 고객을 사로잡을 참신한 캠페인과 전략을 기획하는 브레인!",
        "strength": "데이터 분석력, 트렌드 감각, 창의적 기획력, 마케팅 마인드",
        "trait": "외향적(E), 직관적(N), 감정형(F), 인식형(P)"
    },
    "글로벌 SCM/구매": {
        "desc": "최적의 원부자재 수급처를 발굴하고 가격 경쟁력과 리스크를 철저히 조율하는 전략적 협상가!",
        "strength": "원가 분석력, 전략적 사고, 단가 협상력, 리스크 관리",
        "trait": "내향적(I), 감각적(S), 사고형(T), 판단형(J)"
    },
    "관세/통관 컨설턴트": {
        "desc": "복잡한 관세법과 FTA 원산지 규정을 정확히 해석해 비용을 절감하고 법적 리스크를 방어하는 전문가!",
        "strength": "법적 규정 해석 능력, 분석력, 정확성, 전문 자격증 연계성",
        "trait": "내향적(I), 감각적(S), 사고형(T), 판단형(J)"
    },
    "무역금융/외환": {
        "desc": "신용장(L/C) 조건 검토, 환율 변동 리스크 관리 및 대금 결제를 안전하게 완결하는 금융 파수꾼!",
        "strength": "금융/회계 마인드, 꼼꼼한 서류 검토, 수치 계산 능력",
        "trait": "내향적(I), 감각적(S), 사고형(T), 판단형(J)"
    }
}

# 20개의 종합 무역 성향 질문 구성
QUESTIONS = [
    {"q": " 새로운 해외 파트너사와의 첫 미팅, 당신이 선호하는 방식은?", "options": [("활기찬 분위기 속에서 아이디어를 주고받는 네트워킹 미팅", "E"), ("사전에 자료를 철저히 검토하고 팩트 위주로 논의하는 미팅", "I")]},
    {"q": " 수입 통관 과정에서 예상치 못한 세관 검류(서류 보완)가 발생했을 때?", "options": [("빠르게 관련 규정을 파악하고 유연하게 대안을 찾아 대처한다.", "P"), ("원인을 철저히 분석하고 향후 동일한 문제가 없도록 매뉴얼을 보완한다.", "J")]},
    {"q": " 해외 시장 조사 리포트를 작성할 때 더 중요하게 생각하는 것은?", "options": [("숫자와 통계 데이터, 그리고 과거 실적 중심의 명확한 분석", "S"), ("앞으로의 시장 성장 잠재력과 트렌드 변화에 대한 직관적 통찰", "N")]},
    {"q": " 바이어와의 가격 협상 중 상대방이 무리한 단가 인하를 요구할 때?", "options": [("원가 구조와 데이터 기반 논리로 상대방의 요구를 조목조목 반박한다.", "T"), ("상대방과의 장기적인 파트너십과 감성적 관계 형성을 우선 고려한다.", "F")]},
    {"q": " 평소 업무를 처리할 때 당신의 스타일은?", "options": [("철저한 일정표와 계획에 따라 단계별로 차근차근 진행한다.", "J"), ("상황 유연성에 맞춰 그때그때 우선순위를 조정하며 유연하게 일한다.", "P")]},
    {"q": " 글로벌 전시회나 출장에 참가하게 되었을 때 가장 설레는 부분은?", "options": [("다양한 국적의 새로운 사람들을 만나고 소통하는 것", "E"), ("현지 시장의 생생한 분위기와 새로운 비즈니스 아이디어를 관찰하는 것", "I")]},
    {"q": " 복잡한 무역 계약서(Terms of Trade) 검토 시 가장 먼저 눈이 가는 곳은?", "options": [("Incoterms 조건과 결제 방식 등 구체적이고 현실적인 리스크 조항", "S"), ("계약 전반에 흐르는 거시적인 협력 비전과 장기적 계약 가능성", "N")]},
    {"q": " 팀 내에서 동료가 업무상 실수를 저질렀을 때 당신의 피드백 방식은?", "options": [("어떤 부분이 잘못되었는지 객관적 팩트 위주로 냉정하게 짚어준다.", "T"), ("동료의 기분이 상하지 않도록 부드럽게 위로하며 격려해 준다.", "F")]},
    {"q": " 갑작스럽게 납기가 촉박한 긴급 선적(Urgent Shipment) 건이 떨어졌다면?", "options": [("당황하지 않고 현재 가용한 자원과 물류 경로를 신속하게 재조정한다.", "P"), ("이미 수립된 비상 대응 프로세스와 원칙에 따라 차분히 처리한다.", "J")]},
    {"q": " 외국어(영어 등)로 비즈니스 이메일을 쓸 때 당신의 태도는?", "options": [("핵심 용건을 명확하고 직관적으로 전달하여 군더더기를 없앤다.", "T"), ("상대방의 문화적 배경과 예의를 갖춘 부드러운 표현을 고민한다.", "F")]},
    {"q": " 새로운 무역 자동화 시스템이나 ERP 도입 교육을 받을 때?", "options": [("직접 프로그램을 만져보며 기능을 익히고 실무 적용 방안을 그린다.", "S"), ("이 시스템이 우리 회사 전체 프로세스에 가져올 혁신적 변화를 본다.", "N")]},
    {"q": " 주말을 앞두고 금요일 오후, 다음 주 업무를 준비하는 방식은?", "options": [("다음 주에 처리해야 할 일들을 요일별, 시간별로 깔끔하게 정리해 둔다.", "J"), ("큰 틀의 목표만 잡아두고 그 주의 흐름에 몸을 맡긴다.", "P")]},
    {"q": " 여러 국가의 바이어들과 동시 다발적으로 연락을 주고받아야 할 때?", "options": [("다양한 채널로 에너지를 얻으며 여러 건을 활기차게 소화한다.", "E"),("혼자 집중할 수 있는 조용한 환경에서 한 건씩 깊이 있게 처리한다.", "I")]},
    {"q": " 글로벌 물류 공급망(SCM) 리스크(예: 해상 운임 폭등) 뉴스를 접했을 때?", "options": [("실제 우리 운송 비용과 마진에 미칠 구체적인 수치를 먼저 계산한다.", "S"), ("이 사태가 글로벌 경제와 향후 무역 트렌드에 미칠 파장을 상상해 본다.", "N")]},
    {"q": " 팀 프로젝트를 이끌거나 중요한 결정을 내려야 할 때 중요하게 보는 기준은?", "options": [("누가 봐도 타당하고 효율적인 논리적 근거와 데이터", "T"), ("함께 일하는 팀원들의 사기와 정서적 만족도", "F")]},
    {"q": " 해외 출장이나 바이어 미팅을 준비할 때?", "options": [("일정, 이동 경로, 미팅 아젠다를 철저하게 계획하고 예외를 최소화한다.", "J"), ("대략적인 큰 틀만 잡고 현지 상황에 따라 즉흥적으로 유연하게 움직인다.", "P")]},
    {"q": " 팀 회의나 브레인스토밍 시간에 당신은 주로 어떤 역할을 맡나요?", "options": [("적극적으로 아이디어를 먼저 제안하고 분위기를 주도한다.", "E"),("다른 사람들의 이야기를 경청하다가 핵심적인 의견을 차분히 낸다.", "I")]},
    {"q": " 새로운 국가로의 수출 판로를 개척하라는 지시를 받았을 때?", "options": [("기존 성공 사례와 검증된 시장 데이터를 바탕으로 안전하게 접근한다.", "S"), ("아무도 가보지 않은 신시장이나 독창적인 마케팅 방식을 시도해 본다.", "N")]},
    {"q": " 업무상 중대한 클레임(Claim)이 발생해 고객이 항의할 때?", "options": [("감정을 배제하고 문제의 원인을 규명한 뒤 계약서 조항대로 해결책을 제시한다.", "T"), ("고객의 불트에 깊이 공감하며 마음을 열 수 있는 우호적 태도를 취한다.", "F")]},
    {"q": " 한 주의 업무 마감 시간이 임박했을 때 당신의 행동 패턴은?", "options": [("마감 기한보다 훨씬 전에 모든 서류와 보고를 완벽하게 끝마친다.", "J"),("마감 직전의 고도의 집중력을 발휘해 순식간에 결과물을 완성한다.", "P")]}
]

# 설문 폼 생성
with st.form("mbti_form"):
    answers = []
    for i, item in enumerate(QUESTIONS):
        st.markdown(f"""
            <div class="question-card">
                <b>Q{i+1}. {item['q']}</b>
            </div>
        """, unsafe_allow_html=True)
        
        choice = st.radio(
            f"질문 {i+1} 선택",
            options=[item['options'][0][0], item['options'][1][0]],
            key=f"q_{i}",
            label_visibility="collapsed"
        )
        
        if choice == item['options'][0][0]:
            answers.append(item['options'][0][1])
        else:
            answers.append(item['options'][1][1])
        st.write("")

    submitted = st.form_submit_button("✨ 내 무역 직무 확인하기")
    if submitted:
        st.session_state.submitted = True

# 결과 분석 및 출력
if st.session_state.submitted:
    e_count = answers.count('E')
    i_count = answers.count('I')
    s_count = answers.count('S')
    n_count = answers.count('N')
    t_count = answers.count('T')
    f_count = answers.count('F')
    j_count = answers.count('J')
    p_count = answers.count('P')

    mbti = ""
    mbti += "E" if e_count >= i_count else "I"
    mbti += "S" if s_count >= n_count else "N"
    mbti += "T" if t_count >= f_count else "F"
    mbti += "J" if j_count >= p_count else "P"

    # 직무 매칭 로직
    if mbti.startswith("E") and "N" in mbti:
        recommended_job = "해외영업" if "P" in mbti else "해외마케팅"
    elif "S" in mbti and "J" in mbti:
        if "I" in mbti:
            recommended_job = "무역물류관리"
        else:
            recommended_job = "글로벌 SCM/구매"
    elif "T" in mbti and "I" in mbti:
        recommended_job = "관세/통관 컨설턴트" if "S" in mbti else "무역금융/외환"
    else:
        recommended_job = "해외영업"

    st.write("---")
    
    st.markdown(f"""
        <div class="result-box">
            <h3>🎉 분석 완료! 취준생님을 위한 맞춤 결과</h3>
            <h1 style="color: #1B4332; font-size: 3.5rem; margin: 15px 0;">{mbti}</h1>
            <hr style="border: 1px solid #52B788; width: 40%; margin: 0 auto;">
            <h3 style="color: #2D6A4F; margin-top: 20px;">추천 무역 직무: <span style="color: #081C15; background-color: #A3D9A5; padding: 2px 10px; border-radius: 6px;">{recommended_job}</span></h3>
            <p style="font-size: 1.1rem; margin-top: 15px; line-height: 1.6;">
                <b>{recommended_job}</b><br>
                {JOBS[recommended_job]['desc']}
            </p>
            <p style="font-size: 1rem; color: #1B4332; margin-top: 10px; background-color: rgba(255,255,255,0.6); padding: 10px; border-radius: 8px;">
                💡 <b>핵심 어필 포인트 (자소서/면접용):</b> {JOBS[recommended_job]['strength']}
            </p>
            <p style="font-size: 0.9rem; color: #40916C; margin-top: 10px;">
                내 성향 지표: {JOBS[recommended_job]['trait']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 테스트하기"):
            st.session_state.submitted = False
            st.rerun()