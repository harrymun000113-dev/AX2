""" 
타이타닉 데이터 필터링, 결측치 정리
age(나이)가 35 이상인 승객 필터링
성별(gender)별로 필터링
titanic_cleaned.csv로 저장
실행방법 : streamlit run 0907-3.py
"""
import pandas as pd
import streamlit as st

st.title("✂️ 타이타닉 데이터 전처리 & 필터링")
st.caption("나이 성별 조건으로 필터링해보고, 결측치를 제거해 새 csv로 저장합니다.")

# 1. 데이터 불러오기
CSV_PATH = 'Titanic.csv'
try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    st.error("❌ Titanic.csv 파일을 찾을 수 없습니다. 같은 폴더에 넣어주세요.")
    st.stop() # 에러가 나면 여기서 코드 실행을 멈춥니다.
else:
    st.metric("원본 데이터 행 개수", f"{len(df)}행")

    st.markdown("---")

    st.subheader("1) 나이 35세 이상 승객")
    over_35 = df[df["Age"]>=35]
    st.write(f"나이 35세 이상 승객 수: **{len(over_35)}명**")
    st.dataframe(over_35[["Name", "Sex", "Age"]].head())

    # 성별 여자 남자 필터링 2컬럼 사용
    st.subheader("2) 성별 필터링 결과")
    female_df = df[df["Sex"] == "female"] 
    male_df = df[df["Sex"] == "male"]

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="여성 승객 수", value=f"{len(female_df)}명") 
    with col2:
        st.metric(label="남성 승객 수", value=f"{len(male_df)}명")

    st.markdown("---")

    # &:and |: or
    st.subheader("3) 다중 조건 필터링")
    # 주의: 조건이 2개 이상일 때는 각 조건을 ()로 묶어줘야 에러가 안 납니다!
    over_35_final = df[(df["Age"] >= 35) & (df["Sex"] == "female")]
    st.write(f"35세 이상이면서 여성인 승객 수: **{len(over_35_final)}명**")
    st.dataframe(over_35_final[["Name", "Sex", "Age"]].head())

    st.markdown("---")

    # 나이의 결측치(NaN) 확인 및 dropna처리
    st.subheader("4) Age 결측치 처리")
    missing_age_count = df["Age"].isna().sum()
    st.write(f"Age 열의 결측치 개수: **{missing_age_count}개**")

    # age 열이 결측치인 행만 골라서 제거한다.
    df_clean = df.dropna(subset=["Age"])

    col1, col2 = st.columns(2)

    with col1: st.metric(label="제거 전", value=f"{len(df)}명") # with 아래는 들여쓰기!
    
    with col2: st.metric(label="제거 후", value=f"{len(df_clean)}명") # 끝에 ") 추가!

  # 5. 정제된 데이터를 파일로 저장하기
# 5-1) 코드가 있는 폴더에 직접 파일로 저장하는 명령어
    output_path = ('titanic_cleaned.csv')
    df_clean.to_csv(output_path, index=False)
    st.success("컴퓨터 폴더에 'titanic_cleaned.csv' 파일이 성공적으로 저장되었습니다! 💾")
    st.dataframe(df_clean.head(), use_container_width=True)
