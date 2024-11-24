import streamlit as st
import json
import pandas as pd
import time
import requests

USERNAME = "Tim"
PASSWORD = "523345"


def login():
    data = {
        "username": st.session_state.username,
        "password": st.session_state.password
    }

    response = requests.get("http://localhost:3003/api/auth", json=data)
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


def render_login_page():
    st.title("App login")
    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")
    btn = st.button("Log in")

    if btn:
        login()


def render_home_page():
    st.title("Home")
    st.markdown(f"Welcome to the app, {st.session_state.name}!")


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
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Select an option", ["Home", "Data"])

    if menu == "Home":
        render_home_page()

    if menu == "Data":
        render_data_page()

    btn = st.sidebar.button("Log out")
    if btn:
        logout()
