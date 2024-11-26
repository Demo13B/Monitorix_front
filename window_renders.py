import streamlit as st
from logic import *


def render_login_page():
    st.title("Monitorix login")
    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")
    btn = st.button("Log in")

    if btn:
        login()


def render_home_page():
    st.title("Home")
    st.markdown(f"Welcome to the Monitorix app, {st.session_state.name}!")


def render_users_page():
    st.title("Users")

    queryUsers()

    st.dataframe(st.session_state.users_df, hide_index=True)


def render_data_page():
    st.title("Data")

    queryData()

    st.dataframe(st.session_state.data_df, hide_index=True)
