import streamlit as st
import openai
import PyPDF2
import docx

# 1. 페이지 설정 (가장 깔끔한 기본 테마)
st.set_page_config(page_title="AI 문서 요약기", layout="centered")

# 2. 사이드바 설정 (API 키 및 모델)
with st.sidebar:
    st.title("⚙️ 설정")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    st.divider()
    
    selected_model = st.selectbox(
        "🤖 AI 모델 선택",
        ("gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"),
        index=0
    )
    st.caption("※ API 키가 있어야 요약 기능이 작동합니다.")

# 3. 메인 화면 헤더
st.title("📄 문서 요약 AI")
st.markdown("길고 복잡한 문서를 업로드하면, AI가 핵심 내용만 깔끔하게 요약해 드립니다.")

# 4. 파일 업로드 위젯 (PDF, DOCX, TXT 지원)
uploaded_file = st.file_uploader("여기에 파일을 드래그하거나 클릭해서 업로드하세요.", type=["pdf", "docx", "txt"])

# 5. 파일 처리 및 텍스트 추출 로직
if uploaded_file is not None:
    # 파일 확장자 확인
    file_extension = uploaded_file.name.split(".")[-1].lower()
    extracted_text = ""
    
    with st.spinner("문서를 읽고 있습니다..."):
        try:
            # TXT 파일 읽기
            if file_extension == "txt":
                extracted_text = uploaded_file.getvalue().decode("utf-8")
                
            # PDF 파일 읽기
            elif file_extension == "pdf":
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text() + "\n"
                    
            # DOCX 파일 읽기
            elif file_extension == "docx":
                doc = docx.Document(uploaded_file)
                for para in doc.paragraphs:
                    extracted_text += para.text + "\n"
            
            st.success("✅ 문서 로딩 완료!")
            
            # 추출된 원본 텍스트 미리보기 (접기/펴기)
            with st.expander("원본 문서 내용 미리보기 (일부)"):
                # 텍스트가 너무 길면 1000자까지만 보여줌
                preview_text = extracted_text[:1000] + ("..." if len(extracted_text) > 1000 else "")
                st.text(preview_text)
                
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
            st.stop()

    # 6. 요약 실행 버튼 및 OpenAI API 호출
    st.divider()
    if st.button("🚀 AI 문서 요약하기", use_container_width=True):
        if not api_key:
            st.warning("👈 왼쪽 사이드바에 OpenAI API Key를 먼저 입력해주세요!")
        elif not extracted_text.strip():
            st.warning("문서에서 텍스트를 찾을 수 없습니다. 내용이 있는 파일인지 확인해주세요.")
        else:
            client = openai.OpenAI(api_key=api_key)
            
            with st.spinner("AI가 문서를 분석하고 요약 중입니다... (문서 길이에 따라 시간이 걸릴 수 있습니다)"):
                try:
                    # 요약을 위한 시스템 프롬프트 설정
                    system_prompt = """
                    당신은 전문적인 문서 요약 어시스턴트입니다. 
                    주어진 문서의 핵심 내용을 파악하고, 읽기 쉽게 불릿 포인트(*)를 사용하여 명확하게 요약해주세요.
                    가장 중요한 결론이나 핵심 주제를 먼저 제시하고, 그 다음 세부 내용을 정리해주세요.
                    """
                    
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"다음 문서를 요약해주세요:\n\n{extracted_text}"}
                        ],
                        # 스트리밍 방식 적용 (결과가 타자 치듯 나옴)
                        stream=True 
                    )
                    
                    st.subheader("💡 AI 요약 결과")
                    # 스트리밍으로 화면에 바로 출력
                    st.write_stream(response)
                    
                except Exception as e:
                    st.error(f"요약 중 오류가 발생했습니다: {e}")