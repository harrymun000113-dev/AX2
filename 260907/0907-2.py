""" 
애니메이션 데이터셋 기초 탐색
pandas head/tail/shape/info/columns 를 사용해서 데이터셋의 기본 정보를
화면에 순서대로 보여주는 스트림릿 앱이다. 
실행 방법 streamlit run 0907-1.py
"""

import pandas as pd
import streamlit as st
import io 

# animes.csv 가져오기
CSV_PATH = 'animes.csv'
upload_file = st.file_uploader('animes.csv 파일을 직접 업로드 할 수 있습니다.', type='csv')

if upload_file is not None: 
    df = pd.read_csv(upload_file)
else:
    try:
        # 이 스크립트와 같은 폴더에 있는 애니메이션 파일을 읽어 온다.
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        # 파일이 없을때 사용자가 무엇을 해야 하는지 화면에 안내한다.
        st.error("❌ 애니메이션 파일을 찾을 수 없습니다.")
        st.info("같은 경로에 파일을 업로드 하거나 csv 파일을 폴더에 넣고 새로고침 하세요.")
        df = None

# df가 제대로 로드되었을 때만 아래 내용을 보여주도록 조건문 추가
if df is not None:
    st.title("📺 애니메이션 데이터셋 기초 탐색")
    st.caption("pandas의 head/tail/shape/info/columns로 데이터셋 기본 정보를 확인합니다.")

    st.subheader("1) head(): 데이터의 앞부분 5행 미리보기")
    st.dataframe(df.head(5), use_container_width=True) # 기본행 5개

    st.subheader("2) tail(): 데이터의 뒷부분 5행 미리보기")
    st.dataframe(df.tail(5), use_container_width=True) # 기본행 5개

    st.subheader("3) shape: (행 갯수, 열 갯수)")
    col1, col2 = st.columns(2)
    with col1 :
        st.metric("행 개수", f"{df.shape[0]}개")
    with col2 :
        st.metric("열 개수", f"{df.shape[1]}개")

    st.subheader("4) columns : 전체 열(컬럼) 이름 목록")
    st.write(list(df.columns))

    st.subheader("5) info(): 각 열의 자료형과 결측치(NaN) 여부 요약")
    # df.info 는 값을 리턴하지 않고 화면에 직접적으로 출력만 해주는 함수라서 
    # io.StringIO() 라는 "메모리 위에 가짜 파일"에 결과를 받아낸 뒤 그 내용을 text로 보여준다.

    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    # 아래 표 형식으로 만드는 코드도 나중에 필요할까봐 남겨둡니다. (오타 dtypes 수정 완료!)
    # info_df = pd.DataFrame({
    #     "타입" : df.dtypes,
    #     "결측치 아닌 개수" : df.notna().sum(),
    #     "결측치 개수" : df.isna().sum()
    # })
    # st.dataframe(info_df, use_container_width=True)
    
    st.success("기초 정보 확인이 끝났습니다. 다음 예제에서 전처리 필터링을 할게요")