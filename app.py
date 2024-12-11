import streamlit as st
from window_renders import *


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    render_login_page()
else:
    if st.session_state.access_rights == 1 or st.session_state.access_rights == 2:
        st.sidebar.title("Monitorix")
        menu = st.sidebar.radio(
            "Label", ["Home", "Users", "Data", "Alerts"], label_visibility="collapsed")

        if menu == "Home":
            render_home_page()

        if menu == "Users":
            render_users_page()

        if menu == "Data":
            render_data_page()

        if menu == "Alerts":
            render_alerts_page()

        btn = st.sidebar.button("Log out")
        if btn:
            logout()

    if st.session_state.access_rights == 3:
        st.sidebar.title("Monitorix")
        menu = st.sidebar.radio(
            "Label", [
                "Home",
                "Users",
                "Data",
                "Alerts",
                "Brigades",
                "Facilities",
                "Alert stats",
                "Add tracker"], label_visibility="collapsed")

        if menu == "Home":
            render_home_page()

        if menu == "Users":
            render_admin_users_page()

        if menu == "Data":
            render_admin_data_page()

        if menu == "Alerts":
            render_alerts_page()

        if menu == "Brigades":
            render_admin_brigades_page()

        if menu == "Facilities":
            render_admin_facilities_page()

        if menu == "Alert stats":
            render_analytics_page()

        if menu == "Add tracker":
            render_tracker_page()

        btn = st.sidebar.button("Log out")
        if btn:
            logout()
