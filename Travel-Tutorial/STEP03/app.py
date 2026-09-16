

st.set_page_config(page_title="YEYAK APP", page_icon="✈️", layout=)

home_page = st.page("view/home.py"), title="홈", icon="🏠", deafult=True)
USA = st.page("view/USA.py", "미국", icon="us")
CHINA = st.page("view/CHINA.py", "중국", icon="cn")
JAPAN = st.page("view/JAPAN.py", "일본", icon="jp")
# 내비게이션 메뉴 가동 (사이드바 메뉴가 자동으로 생김)

st.navigation([home, USA, CHINA, JAPAN], default=)
pg.runcd