import streamlit as st
import json
import pandas as pd
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

users_column_renamer = {
    "login": "Login",
    "first_name": "Name",
    "last_name": "Surname",
    "gender": "Gender",
    "phone_number": "Phone number",
    "profession": "Profession",
    "role": "Role",
    "brigade": "Brigade",
    "facility": "Facility",
    "tracker": "Tracker"
}


def login():
    st.session_state.data = {
        "username": st.session_state.username,
        "password": st.session_state.password
    }

    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/auth',
            json=st.session_state.data
        )
    except:

        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.logged_in = True
        st.session_state.name = body["first_name"]
        st.session_state.access_rights = body["access_rights"]
        st.success("Login successful")
        time.sleep(1)
        st.rerun()
    else:
        st.error("Wrong username or password")


def logout():
    st.session_state.logged_in = False
    st.rerun()


def queryUsers():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/users',
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return
    if (response.status_code == 200):
        body = response.json()
        st.session_state.users_df = pd.DataFrame(
            body).rename(columns=users_column_renamer)
    else:
        st.error("Unauthorized")


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
