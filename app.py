import streamlit as st
from window_renders import *


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    render_login_page()
else:
    if st.session_state.access_rights == 1:
        st.sidebar.title("Monitorix")
        menu = st.sidebar.radio(
            "Label", ["Home", "Users"], label_visibility="collapsed")

        if menu == "Home":
            render_home_page()

        if menu == "Users":
            render_users_page()

        btn = st.sidebar.button("Log out")
        if btn:
            logout()

    # st.sidebar.title("Menu")
    # menu = st.sidebar.radio("Select an option", ["Home", "Data"])

    # if menu == "Home":
    #     render_home_page()

    # if menu == "Data":
    #     render_data_page()

    # btn = st.sidebar.button("Log out")
    # if btn:
    #     logout()
