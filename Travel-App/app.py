import streamlit as st
import sys
import os

# Add src to python path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data import TRAVEL_DATA
from components.country_card import render_country_card

def main():
    st.set_page_config(
        page_title="Global Travel Guide",
        page_icon="✈️",
        layout="wide"
    )

    # Sidebar Navigation
    st.sidebar.title("🌍 여행 가이드")
    st.sidebar.markdown("탐색하고 싶은 나라를 선택하세요.")
    
    # Home is South Korea by default
    countries = list(TRAVEL_DATA.keys())
    selected_country = st.sidebar.radio("국가 선택", countries, index=0)

    # Header
    st.title(f"✈️ {selected_country} 여행 정보")
    
    if selected_country == "대한민국":
        st.write("### 환영합니다! 대한민국의 구석구석을 소개합니다.")
    
    # Render Country Content
    if selected_country in TRAVEL_DATA:
        render_country_card(selected_country, TRAVEL_DATA[selected_country])
    
    # Footer
    st.sidebar.divider()
    st.sidebar.info("이 서비스는 Streamlit으로 제작되었습니다.")

if __name__ == "__main__":
    main()
