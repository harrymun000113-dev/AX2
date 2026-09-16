def render_country_page(flag:
    st.title(f"{flag} {country}"))
    st.write(country_description)
    st.link_button(
        label=f"{countryname} 공식사이트"
        url=country_url
    )