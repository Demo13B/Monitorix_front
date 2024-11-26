import streamlit as st
import requests
import os
import time
import pandas as pd
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

data_column_renamer = {
    "login": "Login",
    "tracker": "Tracker",
    "description": "Description",
    "air_pressure": "Air pressure",
    "pulse": "Pulse",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "activity": "Activity",
    "fall": "Fall",
    "temperature": "Temperature",
    "humidity": "Humidity",
    "charge": "Charge",
    "analyzer_alarm": "Alarm",
    "time": "Time"
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


def queryData():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/data',
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return
    if (response.status_code == 200):
        body = response.json()
        st.session_state.data_df = pd.DataFrame(
            body).rename(columns=data_column_renamer)
    else:
        st.error("Unauthorized")
