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
    st.matrix("원본 데이터 행 개수", f"{len(df)}행")

    st.markdown("---")

    st.subheader("1) 나이 35세 이상 승객")
    over_35 = df[df["age"]>=35]
    st.write(f"나이 35세 이상 승객 수:**{len(over_35)}명**")
    

# 2. 결측치 정리 (빈칸 처리)
st.subheader("1) 결측치 정리 (나이 비어있는 칸 삭제)")
# 나이(Age) 컬럼에 빈칸(NaN)이 있는 승객은 지워버립니다.
df_cleaned = df.dropna(subset=['Age']) 
st.write(f"✔️ 나이 정보가 없는 승객을 지워서 총 {len(df)}명에서 **{len(df_cleaned)}명**으로 줄었습니다.")

# 3. 데이터 필터링 (나이 35세 이상)
st.subheader("2) 나이 35세 이상 승객 필터링")
df_age_filtered = df_cleaned[df_cleaned['Age'] >= 35]
st.write(f"✔️ 35세 이상 승객은 총 **{len(df_age_filtered)}명**입니다.")

# 4. 데이터 필터링 (성별 선택)
st.subheader("3) 성별(Sex)로 한 번 더 필터링")
# 타이타닉 원본 데이터에는 성별이 'Sex'라는 이름으로 들어있습니다.
gender_choice = st.selectbox("원하는 성별을 선택하세요", ['male', 'female'])

# 위에서 나이로 거른 데이터에 성별 필터링을 한 번 더 씌웁니다.
df_final = df_age_filtered[df_age_filtered['Sex'] == gender_choice]

st.dataframe(df_final, use_container_width=True)
st.info(f"👉 35세 이상이면서 '{gender_choice}'인 승객은 총 **{len(df_final)}명**입니다.")

# 5. 정제된 데이터를 파일로 저장하기
st.subheader("4) titanic_cleaned.csv 로 저장하기")

# 5-1) 코드가 있는 폴더에 직접 파일로 저장하는 명령어
df_final.to_csv('titanic_cleaned.csv', index=False)
st.success("컴퓨터 폴더에 'titanic_cleaned.csv' 파일이 성공적으로 저장되었습니다! 💾")

# 5-2) (보너스) 웹 화면에서 버튼을 눌러 다운로드하게 만들기
csv_data = df_final.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 정제된 데이터 직접 다운로드하기",
    data=csv_data,
    file_name='titanic_cleaned.csv',
    mime='text/csv')