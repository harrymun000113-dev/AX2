#인코딩 자동 감지 + 한글 폰트 막대그래프
# 여러 인코딩("ftf-8-sig"), "cp949", "euc-kr" 순서대로 시도
# 내가 쓸 폰트 같은 경로에 있어야 함
# 막대그래프 생성후 그림으로 저장 .png
# 실행 streamlit run 0907-05.py
import os 
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib import font_manager

st.title("📊 인코딩 자동 감지 + 한글 폰트 막대그래프 (Titanic 연습)")
st.caption("여러 인코딩을 순서대로 시도해서 파일을 읽고, 객실등급별 생존율을 그래프로 그립니다")
 #여기서 부터 시작해라라는 의미
CSV_PATH = os.path.join(os.path.dirname(__file__),"titanic_cleaned.csv")
FONT_PATH = os.path.join(os.path.dirname(__file__),"NanumGothic.otf")

CSV_PATH = 'titanic_cleaned.csv'

# 시도할 인코딩 목록 (utf-8-sig -> cp949 -> euc-kr)
encodings = ['utf-8-sig', 'cp949', 'euc-kr']


def load_csv_with_encodings(file_path):
    encodings = ['utf-8-sig', 'cp949', 'euc-kr']
    for enc in encodings:
        try:
            return pd.read_csv(file_path, encoding=enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return None

# 사용 예시
df = load_csv_with_encodings('Titanic.csv')

if df is not None:
    st.success("데이터 불러오기 성공!")
    st.dataframe(df.head())
else:
    st.error("파일을 읽을 수 없거나 지원하는 인코딩이 아닙니다.")

# 인코딩 자동 감지로 Csv읽기
st.subheader("1) 인코딩 자동 감지")
df = load_csv_with_encodings(CSV_PATH)

st.markdown("---")
# 객실등급(Pclass) 별 생존율 집계
# 사망0 /생존1 / 등급별 평균을 내면
# 그대로가 등급의 생존 비율이다.
# 10명 남 3 여자 7
# 1000명 생존 300 300/1000 30%


pclass_survived_rate = df.groupby("Pclass")["Survived"].mean().sort_index()
st.dataframe((pclass_survived_rate * 100).round(1).rename("생존율(%)"))
# df_df = st.dataframe( pclass_survived_rate * 100).round(1).rename("생존율(%)")
#st.write(df_df)


st.markdown("---")
# 차트 그리기
st.subheader("3) 객실 등급별 생존율 막대그래프")
try:
    # 폰트 파일이 없으면 FilenotFoundError 발생 
    font_prop = font_manager.FontProperties(fname=FONT_PATH)
    #matplotlib font_manager에 폰트를 등록하고, 전역 폰트로 설정
    font_manager.fontManager.addfont(FONT_PATH)
    plt.rcParams["font.family"] = font_prop.get_name()
    st.write("NanumGothic 폰트를 적용했습니다.")
except FileNotFoundError:
    st.warning("폰트 파일을 찾을 수 없습니다.")

fig, ax = plt.subplots(figsize=(8,5))
(pclass_survived_rate * 100).plot(kind="bar", color="red")
ax.set_title("객실 등급별 생존율")
ax.set_xlabel("객실등급(Pclass)")
ax.set_ylabel("생존율(%)")

st.pyplot(fig)

output_png = output_path = os.path.join(os.path.dirname(__file__), "chart.png")
fig.savefig(output_png)
st.success("저장에 성공했습니다!")