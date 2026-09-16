import streamlit as st

def render_country_card(country_name, country_info):
    """
    Renders a stylized card for a country.
    """
    with st.container():
        st.subheader(f"{country_name} ({country_info['name_en']})")
        
        # Display the generated image
        st.image(country_info['image_path'], use_container_width=True)
        
        # Description with custom styling
        st.markdown(f"""
            <div style="
                padding: 15px;
                border-radius: 10px;
                background-color: #f0f2f6;
                margin-bottom: 20px;
                color: #31333F;
            ">
                {country_info['description']}
            </div>
        """, unsafe_allow_html=True)
        
        # Link button
        st.markdown(f"""
            <a href="{country_info['link']}" target="_blank" style="
                text-decoration: none;
                display: inline-block;
                padding: 10px 20px;
                background-color: #FF4B4B;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            ">
                ✈️ {country_name} 공식 여행 사이트로 이동
            </a>
        """, unsafe_allow_html=True)
        
        st.divider()
