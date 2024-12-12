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

alerts_column_renamer = {
    "login": "Login",
    "tracker": "Tracker",
    "message": "Alert",
    "type": "Type"
}

brigades_column_renamer = {
    "name": "Name",
    "brigadier_name": "Brigadier name",
    "brigadier_surname": "Brigadier surname",
    "facility_name": "Facility",
    "latitude": "Latitude",
    "longitude": "Longitude"
}

facilities_column_renamer = {
    "name": "Name",
    "latitude": "Latitude",
    "longitude": "Longitude"
}


def color_alerts(s):
    return ['background-color: yellow'] * len(s) if s.Type == 1 else ['background-color: red'] * len(s)


def logout():
    st.session_state.logged_in = False
    st.session_state.last_data = None
    st.session_state.users_df = None
    st.session_state.data_df = None
    st.session_state.brigades_df = None
    st.session_state.facilities_ds = None
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
        st.error("Something went wrong")


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
        st.error("Something went wrong")


def queryLastData():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/data/' + str(st.session_state.id),
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        if len(body) != 0:
            st.session_state.last_data = body[0]
    else:
        st.error("Something went wrong")


def queryAlerts():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/alerts',
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        df = pd.DataFrame(body).rename(columns=alerts_column_renamer)
        st.session_state.alerts_df = df.style.apply(color_alerts, axis=1)
    else:
        st.error("Something went wrong")


def queryBrigades():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/brigades',
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.brigades_df = pd.DataFrame(
            body).rename(columns=brigades_column_renamer)
    else:
        st.error("Something went wrong")


def queryFacilities():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/facilities',
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.facilities_df = pd.DataFrame(
            body).rename(columns=facilities_column_renamer)
    else:
        st.error("Something went wrong")


def queryStats():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/alerts/stats/users',
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.user_stats_df = pd.DataFrame(body)
    else:
        st.error("Something went wrong")

    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/alerts/stats/brigades',
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.brigade_stats_df = pd.DataFrame(body)
    else:
        st.error("Something went wrong")

    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/alerts/stats/facilities',
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.facility_stats_df = pd.DataFrame(body)
    else:
        st.error("Something went wrong")


def insert_facility(facility: dict):
    data = {
        "username": st.session_state.data["username"],
        "password": st.session_state.data["password"],
        "facility": facility
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/facilities',
            json=data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("Facility added")
    else:
        st.error("Something went wrong")


def insert_brigade(brigade):
    data = {
        "username": st.session_state.data["username"],
        "password": st.session_state.data["password"],
        "brigade": brigade
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/brigades',
            json=data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("Brigade added")
    else:
        st.error("Something went wrong")


def insert_tracker(tracker):
    data = {
        "username": st.session_state.data["username"],
        "password": st.session_state.data["password"],
        "tracker": tracker
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/trackers',
            json=data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("Tracker added")
    else:
        st.error("Something went wrong")


def insert_user(user):
    data = {
        "username": st.session_state.data["username"],
        "password": st.session_state.data["password"],
        "user": user
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/users',
            json=data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("User added")
    else:
        st.error("Something went wrong")


def insertData(data):
    body = {
        "username": st.session_state.data["username"],
        "password": st.session_state.data["password"],
        "data": data
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/data',
            json=body
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("Tracker data added")
    else:
        st.error("Something went wrong")


def deleteUser(login: str):
    body = {
        "username": st.session_state.data["username"],
        "password": st.session_state.data["password"],
        "login": login
    }

    try:
        response = requests.delete(
            str(os.getenv("API_URI")) + '/api/users',
            json=body
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        st.success("User removed")
    else:
        st.error("Something went wrong")


def deleteBrigade(name: str):
    body = {
        "username": st.session_state.data["username"],
        "password": st.session_state.data["password"],
        "name": name
    }

    try:
        response = requests.delete(
            str(os.getenv("API_URI")) + '/api/brigades',
            json=body
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        st.success("Brigade removed")
    else:
        st.error("Something went wrong")


def deleteFacility(name: str):
    body = {
        "username": st.session_state.data["username"],
        "password": st.session_state.data["password"],
        "name": name
    }

    try:
        response = requests.delete(
            str(os.getenv("API_URI")) + '/api/facilities',
            json=body
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        st.success("Facility removed")
    else:
        st.error("Something went wrong")


def deleteTracker(mac: str):
    body = {
        "username": st.session_state.data["username"],
        "password": st.session_state.data["password"],
        "mac": mac
    }

    try:
        response = requests.delete(
            str(os.getenv("API_URI")) + '/api/trackers',
            json=body
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        st.success("Tracker and it's data removed")
    else:
        st.error("Something went wrong")


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
        st.session_state.id = body["user_id"]
        st.session_state.name = body["first_name"]
        st.session_state.access_rights = body["access_rights"]
        st.success("Login successful")
        queryAlerts()
        queryBrigades()
        queryData()
        queryFacilities()
        queryLastData()
        queryStats()
        queryUsers()

        time.sleep(1)
        st.rerun()
    else:
        st.error("Wrong username or password")
