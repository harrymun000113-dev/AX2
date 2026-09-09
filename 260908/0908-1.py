# -*- coding: utf-8 -*-
import os
import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 디자인 (가로로 넓게 설정, 제목 및 아이콘 추가)
st.set_page_config(
    page_title="반도체류 수출 실적 대시보드",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS를 통한 앱 디자인 고도화
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 메인 화면 헤더
st.markdown('<div class="main-title">📈 반도체류(HS 85) 수출 실적 대시보드</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">미국 및 베트남 대상 실제 수출 실적이 있는 상위 10건 데이터 분석 및 리포트 생성</div>', unsafe_allow_html=True)

# 3. 데이터 로드 함수 (캐싱 적용으로 속도 향상)
@st.cache_data
def load_data(file_path):
    encodings = ['utf-8', 'utf-8-sig', 'cp949', 'euc-kr']
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
        except Exception as e:
            st.error(f"데이터 로드 중 에러 발생: {e}")
            return None
    return None

csv_file = 'raw_trade_data.csv'

if not os.path.exists(csv_file):
    st.error(f"❌ '{csv_file}' 파일이 존재하지 않습니다. 파이썬 파일과 동일한 경로에 파일을 위치시켜 주세요.")
else:
    df = load_data(csv_file)
    
    if df is not None:
        try:
            # 4. 데이터 필터링 및 전처리
            # 조건 1: hs_code가 '85'로 시작하는 반도체류 (문자열 변환 후 접두사 매칭)
            cond_hs = df['hs_code'].astype(str).str.startswith('85')
            
            # 조건 2: 국가명이 미국 또는 베트남
            cond_country = df['국가명'].isin(['미국', '베트남'])
            
            # 조건 3: 수출금액이 0보다 큰 수 (실제 수출실적이 있는 행)
            cond_amount = df['수출금액'] > 0
            
            # 전체 조건 결합
            filtered_df = df[cond_hs & cond_country & cond_amount].copy()
            
            # 5. 수출금액 기준 상위 10건 정렬
            top10_df = filtered_df.sort_values(by='수출금액', ascending=False).head(10)
            
            # 인덱스를 1부터 시작하도록 깔끔하게 재설정
            top10_df = top10_df.reset_index(drop=True)
            top10_df.index = top10_df.index + 1
            
            # 6. 정렬 결과를 report.csv로 영구 저장 (한글 깨짐 방지를 위해 utf-8-sig 인코딩 사용)
            top10_df.to_csv('report.csv', index=False, encoding='utf-8-sig')
            
            # 7. 대시보드 레이아웃 구성
            # 상단 주요 지표 (Metrics) 시각화
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="총 필터링 건수 (미국/베트남 HS85)", 
                    value=f"{len(filtered_df):,} 건"
                )
            with col2:
                total_top10_export = top10_df['수출금액'].sum()
                st.metric(
                    label="상위 10건 총 수출액 ($)", 
                    value=f"${total_top10_export:,.0f}"
                )
            with col3:
                max_export = top10_df['수출금액'].max()
                st.metric(
                    label="최대 단일 수출액 ($)", 
                    value=f"${max_export:,.0f}"
                )
            with col4:
                avg_export = top10_df['수출금액'].mean()
                st.metric(
                    label="상위 10건 평균 수출액 ($)", 
                    value=f"${avg_export:,.0f}"
                )
            
            st.markdown("---")
            
            # 데이터 그리드 및 그래프 배치 (1:1 분할)
            left_col, right_col = st.columns(2)
            
            with left_col:
                st.subheader("📋 수출 실적 상위 10건 상세 리스트")
                # 숫자 포맷이 적용된 데이터프레임 렌더링
                formatted_df = top10_df.copy()
                # 뷰어용으로 금액 포맷팅 적용
                formatted_df['수출금액_포맷'] = formatted_df['수출금액'].apply(lambda x: f"${x:,.0f}")
                formatted_df['중량_포맷'] = formatted_df['중량'].apply(lambda x: f"{x:,.2f} kg")
                
                # 원본 컬럼 대신 예쁜 컬럼 위주로 보여주기
                display_df = formatted_df[['날짜', 'hs_code', '품목명', '국가명', '수출입구분', '수출금액_포맷', '중량_포맷']]
                display_df.columns = ['날짜', 'HS코드', '품목명', '국가명', '수출입구분', '수출금액', '중량']
                
                st.dataframe(display_df, use_container_width=True)
                
                # 리포트 다운로드 및 저장 상태 안내
                st.info("💡 위 데이터는 이미 `report.csv` 파일로 자동 저장되었습니다.")
                
                # 로컬 다운로드 버튼 제공
                csv_data = top10_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                st.download_button(
                    label="📥 필터링 결과 리포트(CSV) 다운로드",
                    data=csv_data,
                    file_name="report.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
            with right_col:
                st.subheader("📊 상위 10건 수출금액 시각화 ($)")
                
                # 그래프용 데이터 가공 (국가명과 품목명을 결합하여 레이블 가독성 증대)
                chart_df = top10_df.copy()
                chart_df['수출 레이블'] = chart_df.apply(
                    lambda row: f"{row['국가명']} ({row['날짜']})", axis=1
                )
                
                # Streamlit 내장 바 차트 사용
                chart_data = chart_df.set_index('수출 레이블')['수출금액']
                st.bar_chart(chart_data, use_container_width=True)
                
            # 8. 부가 분석: 국가별 비율 시각화
            st.markdown("---")
            country_summary = top10_df.groupby('국가명')['수출금액'].agg(['sum', 'count']).reset_index()
            country_summary.columns = ['국가명', '총 수출액 ($)', '상위 10건 중 건수']
            
            st.subheader("🇺🇸🇻🇳 국가별 수출 요약 (상위 10건 기준)")
            st.table(country_summary.style.format({
                '총 수출액 ($)': lambda x: f"${x:,.0f}"
            }))
            
            st.success("✅ 'report.csv' 파일 생성 및 화면 렌더링이 성공적으로 수행되었습니다.")
            
        except KeyError as ke:
            st.error(f"❌ 데이터 컬럼명이 일치하지 않습니다. 오류 컬럼: {ke}")
            st.info("실제 CSV 컬럼 구성: " + ", ".join(df.columns))
        except Exception as e:
            st.error(f"❌ 처리 중 알 수 없는 에러가 발생했습니다: {e}")
