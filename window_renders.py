import streamlit as st
import requests
import json
import pandas as pd
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

    try:
        response = requests.get(
            "http://localhost:3003/api/users",
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return

    body = response.json()
    st.session_state.users_df = pd.DataFrame(
        body).rename(columns=users_column_renamer)

    st.dataframe(st.session_state.users_df, hide_index=True)


def render_data_page():
    st.title("Data")

    json_string = '''[{"name":"Tim", "gender":"male"}, {"name":"Bertha", "gender":"female"}]'''
    json_object = json.loads(json_string)

    df = pd.DataFrame(json_object)

    st.dataframe(df, hide_index=True)
