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
    "type": "Type",
    "time": "Time"
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
    st.session_state.alerts_df = None
    st.session_state.facilities_df = None
    st.session_state.user_stats_df = None
    st.session_state.brigade_stats_df = None
    st.session_state.facility_stats_df = None
    st.session_state.tracker_names = None
    st.session_state.brigade_names = None

    try:
        response = requests.post(os.getenv('API_URI') + '/api/auth/logout',
                                 cookies=st.session_state.cookies)
    except:
        st.error('Could not logout')
        return

    st.session_state.cookies = None

    st.rerun()


def refresh():
    try:
        response = requests.post(os.getenv('API_URI') + '/api/auth/refresh',
                                 cookies=st.session_state.cookies)
    except:
        st.error('Could not refresh')

    if (response.status_code == 200):
        st.session_state.cookies = response.cookies
    else:
        login()


def queryUsers():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/users',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.users_df = pd.DataFrame(
            body).rename(columns=users_column_renamer)
    elif (response.status_code == 401):
        refresh()
        queryUsers()
    else:
        st.error("Something went wrong")


def queryData():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/data',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return
    if (response.status_code == 200):
        body = response.json()
        df = pd.DataFrame(body).rename(columns=data_column_renamer)

        if (not df.empty):
            df['Time'] = pd.to_datetime(df['Time'])
            df['Time'] = df['Time'].dt.tz_convert('Etc/GMT-3')
            df['Time'] = df['Time'].dt.tz_localize(None)

        st.session_state.data_df = df
    elif (response.status_code == 401):
        refresh()
        queryData()
    else:
        st.error("Something went wrong")


def queryLastData():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/data/' + str(st.session_state.id),
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        if len(body) != 0:
            st.session_state.last_data = body[0]
    elif (response.status_code == 401):
        refresh()
        queryLastData()
    else:
        st.error("Something went wrong")


def queryAlerts():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/alerts',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        df = pd.DataFrame(body).rename(columns=alerts_column_renamer)
        if (not df.empty):
            df['Time'] = pd.to_datetime(df['Time'])
            df['Time'] = df['Time'].dt.tz_convert('Etc/GMT-3')
            df['Time'] = df['Time'].dt.tz_localize(None)
        st.session_state.alerts_df = df.style.apply(color_alerts, axis=1)
    elif (response.status_code == 401):
        refresh()
        queryAlerts()
    else:
        st.error("Something went wrong")


def queryBrigades():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/brigades',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.brigades_df = pd.DataFrame(
            body).rename(columns=brigades_column_renamer)
    elif (response.status_code == 401):
        refresh()
        queryBrigades()
    else:
        st.error("Something went wrong")


def queryFacilities():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/facilities',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.facilities_df = pd.DataFrame(
            body).rename(columns=facilities_column_renamer)
    elif (response.status_code == 401):
        refresh()
        queryFacilities()
    else:
        st.error("Something went wrong")


def queryStats():
    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/alerts/stats/users',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.user_stats_df = pd.DataFrame(body)
    elif (response.status_code == 401):
        refresh()
        queryStats()
    else:
        st.error("Something went wrong")

    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/alerts/stats/brigades',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.brigade_stats_df = pd.DataFrame(body)
    elif (response.status_code == 401):
        refresh()
        queryStats()
    else:
        st.error("Something went wrong")

    try:
        response = requests.get(
            os.getenv("API_URI") + '/api/alerts/stats/facilities',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.facility_stats_df = pd.DataFrame(body)
    elif (response.status_code == 401):
        refresh()
        queryStats()
    else:
        st.error("Something went wrong")


def insert_facility(facility: dict):
    data = {
        "facility": facility
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/facilities',
            json=data,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("Facility added")
    elif (response.status_code == 401):
        refresh()
        insert_facility(facility)
    else:
        st.error("Something went wrong")


def insert_brigade(brigade):
    data = {
        "brigade": brigade
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/brigades',
            json=data,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("Brigade added")
    elif (response.status_code == 401):
        refresh()
        insert_brigade(brigade)
    else:
        st.error("Something went wrong")


def insert_tracker(tracker):
    data = {
        "tracker": tracker
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/trackers',
            json=data,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("Tracker added")
    elif (response.status_code == 401):
        refresh()
        insert_tracker(tracker)
    else:
        st.error("Something went wrong")


def insert_user(user):
    data = {
        "user": user
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/users',
            json=data,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("User added")
    elif (response.status_code == 401):
        refresh()
        insert_user(user)
    else:
        st.error("Something went wrong")


def insertData(data):
    body = {
        "data": data
    }

    try:
        response = requests.post(
            str(os.getenv("API_URI")) + '/api/data',
            json=body,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 201):
        st.success("Tracker data added")
    elif (response.status_code == 401):
        refresh()
        insertData(data)
    else:
        st.error("Something went wrong")


def deleteUser(login: str):
    body = {
        "login": login
    }

    try:
        response = requests.delete(
            str(os.getenv("API_URI")) + '/api/users',
            json=body,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        st.success("User removed")
    elif (response.status_code == 401):
        refresh()
        deleteUser(login)
    else:
        st.error("Something went wrong")


def deleteBrigade(name: str):
    body = {
        "name": name
    }

    try:
        response = requests.delete(
            str(os.getenv("API_URI")) + '/api/brigades',
            json=body,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        st.success("Brigade removed")
    elif (response.status_code == 401):
        refresh()
        deleteBrigade(name)
    else:
        st.error("Something went wrong")


def deleteFacility(name: str):
    body = {
        "name": name
    }

    try:
        response = requests.delete(
            str(os.getenv("API_URI")) + '/api/facilities',
            json=body,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        st.success("Facility removed")
    elif (response.status_code == 401):
        refresh()
        deleteFacility(name)
    else:
        st.error("Something went wrong")


def deleteTracker(mac: str):
    body = {
        "mac": mac
    }

    try:
        response = requests.delete(
            str(os.getenv("API_URI")) + '/api/trackers',
            json=body,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        st.success("Tracker and it's data removed")
    elif (response.status_code == 401):
        refresh()
        deleteTracker(mac)
    else:
        st.error("Something went wrong")


def closeAlerts(login: str):
    body = {
        "login": login
    }

    try:
        response = requests.delete(
            str(os.getenv("API_URI")) + '/api/alerts',
            json=body,
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        st.success("Alerts closed")
    elif (response.status_code == 401):
        refresh()
        closeAlerts(login)
    else:
        st.error("Something went wrong")


def queryTrackerNames():
    try:
        response = requests.get(
            str(os.getenv("API_URI")) + '/api/trackers',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        res_body: list = response.json()

        res_body.append(None)

        st.session_state.tracker_names = res_body
    elif (response.status_code == 401):
        refresh()
        queryTrackerNames()
    else:
        st.error("Something went wrong")


def queryBrigadeNames():
    try:
        response = requests.get(
            str(os.getenv("API_URI")) + '/api/brigades/names',
            cookies=st.session_state.cookies
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        res_body: list = response.json()

        res_body.append(None)

        st.session_state.brigade_names = res_body
    elif (response.status_code == 401):
        refresh()
        queryBrigadeNames()
    else:
        st.error("Something went wrong")


def login():
    st.session_state.data = {
        "username": st.session_state.username,
        "password": st.session_state.password
    }

    try:
        response = requests.post(
            os.getenv("API_URI") + '/api/auth/login',
            json=st.session_state.data
        )
    except:
        st.error("Server is down")
        return

    if (response.status_code == 200):
        body = response.json()
        st.session_state.cookies = response.cookies
        st.session_state.logged_in = True
        st.session_state.id = body["user_id"]
        st.session_state.name = body["first_name"]
        st.session_state.access_rights = body["access_rights"]
        st.success("Login successful")

        if st.session_state.access_rights == 3:
            queryAlerts()
            queryBrigades()
            queryData()
            queryFacilities()
            queryLastData()
            queryStats()
            queryUsers()
            queryTrackerNames()
            queryBrigadeNames()

        time.sleep(1)
        st.rerun()
    else:
        st.error("Wrong username or password")
