import streamlit as st
import matplotlib.pyplot as plt
from logic import *
from datetime import datetime


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

    queryLastData()

    st.subheader("Last data")

    if "last_data" not in st.session_state or st.session_state.last_data == None:
        st.markdown("No data available")
        return

    data = st.session_state.last_data

    st.markdown(f"Time: {data["time"]}")
    st.markdown(f"Login: {data["login"]}")
    st.markdown(f"Tracker: {data["tracker"]}")
    st.markdown(f"Description: {data["description"]}")
    st.markdown(f"Air pressure: {data["air_pressure"]}")
    st.markdown(f"Temperature: {data["temperature"]} °C")
    st.markdown(f"Humidity: {data["humidity"]} %")
    st.markdown(f"Pulse: {data["pulse"]} bpm")
    st.markdown(f"Latitude: {data["latitude"]}")
    st.markdown(f"Longitude: {data["longitude"]}")

    if data["activity"]:
        st.markdown("Activity: Yes")
    else:
        st.markdown("Activity: No")

    if data["fall"]:
        st.markdown("Fall: Yes")
    else:
        st.markdown("Fall: No")

    if data["analyzer_alarm"]:
        st.markdown("Analyzer alarm: Yes")
    else:
        st.markdown("Analyzer alarm: No")

    st.markdown(f"Charge: {data["charge"]} %")

    btn = st.button("Update")

    if btn:
        st.rerun()


def render_users_page():
    st.title("Users")

    queryUsers()

    st.dataframe(st.session_state.users_df, hide_index=True)

    btn = st.button("Update")

    if btn:
        st.rerun()


def render_data_page():
    st.title("Data")

    queryData()

    st.dataframe(st.session_state.data_df, hide_index=True)

    btn = st.button("Update")

    if btn:
        st.rerun()


def render_alerts_page():
    st.title("Alerts")

    queryAlerts()

    st.dataframe(st.session_state.alerts_df, hide_index=True)

    btn = st.button("Update")

    if btn:
        st.rerun()


def render_brigades_page():
    st.title("Brigades")

    queryBrigades()

    st.dataframe(st.session_state.brigades_df, hide_index=True)

    btn = st.button("Update")

    if btn:
        st.rerun()


def render_facilities_page():
    st.title("Facilities")

    queryFacilities()

    st.dataframe(st.session_state.facilities_df, hide_index=True)

    btn = st.button("Update")

    if btn:
        st.rerun()


def render_analytics_page():
    st.title("Alert stats")

    queryStats()

    tab1, tab2, tab3 = st.tabs(["By user", "By brigade", "By facility"])

    with tab1:
        st.dataframe(st.session_state.user_stats_df, hide_index=True)

    with tab2:
        st.dataframe(st.session_state.brigade_stats_df, hide_index=True)

    with tab3:
        st.dataframe(st.session_state.facility_stats_df, hide_index=True)

    btn = st.button("Update")

    if btn:
        st.rerun()


def render_admin_facilities_page():
    st.title("Facilities")
    tab1, tab2 = st.tabs(["Facilities", "Add facility"])

    with tab1:
        queryFacilities()
        st.dataframe(st.session_state.facilities_df, hide_index=True)

        btn = st.button("Update")

        if btn:
            st.rerun()

    with tab2:
        facility = {}

        facility["name"] = st.text_input("Facility name")
        facility["latitude"] = st.number_input("Latitude")
        facility["longitude"] = st.number_input("Longitude")

        btn = st.button("Add")

        if btn:
            insert_facility(facility)


def render_admin_brigades_page():
    st.title("Brigades")

    tab1, tab2, tab3 = st.tabs(["Brigades", "Add brigade", "Remove brigade"])

    queryBrigades()

    with tab1:
        st.dataframe(st.session_state.brigades_df, hide_index=True)

        btn = st.button("Update")

        if btn:
            st.rerun()

    with tab2:
        brigade = {}

        brigade["name"] = st.text_input("Brigade name")
        brigade["facility_name"] = st.selectbox(
            "Facility", st.session_state.facilities_df["Name"].unique())

        btn = st.button("Add")

        if btn:
            insert_brigade(brigade)

    with tab3:
        name = st.selectbox(
            "Choose brigade to delete", st.session_state.brigades_df["Name"].unique(
            )
        )

        btn = st.button("Remove")

        if btn:
            deleteBrigade(name)


def render_tracker_page():
    st.title("Add tracker")

    tracker = {}

    tracker['mac_address'] = st.text_input("Mac Address")
    tracker['description'] = st.text_input("Description")

    btn = st.button("Add")

    if btn:
        insert_tracker(tracker)


def render_admin_users_page():
    st.title("Users")

    tab1, tab2, tab3 = st.tabs(["Users", "Add user", "Remove user"])

    queryUsers()

    with tab1:
        st.dataframe(st.session_state.users_df, hide_index=True)

        btn = st.button("Update")

        if btn:
            st.rerun()

    with tab2:
        user = {}

        user["login"] = st.text_input("Username")
        user["password"] = st.text_input("Password", type="password")
        user["gender"] = st.selectbox("Gender", ("male", "female", "other"))
        user["first_name"] = st.text_input("First Name")
        user["last_name"] = st.text_input("Last Name")
        user["phone_number"] = st.text_input("Phone number")
        user["profession"] = st.text_input("Profession")
        user["role"] = st.selectbox("Role", ("Admin", "Brigadier", "Worker"))

        brigade = st.selectbox(
            "Brigade", st.session_state.users_df["Brigade"].unique())
        tracker = st.selectbox("Tracker MAC Adress",
                               st.session_state.users_df["Tracker"].unique())

        btn = st.button("Add")

        if btn:
            if (brigade != None):
                user["brigade"] = brigade
            if (tracker != None):
                user["tracker"] = tracker

            insert_user(user)

    with tab3:
        login = st.selectbox("Choose user to delete",
                             st.session_state.users_df["Login"].unique()
                             )
        btn = st.button("Remove")

        if btn:
            deleteUser(login)


def render_admin_data_page():
    st.title("Data")

    tab1, tab2 = st.tabs(["Data", "Add data"])

    with tab1:
        queryData()
        st.dataframe(st.session_state.data_df, hide_index=True)

        btn = st.button("Update")

        if btn:
            st.rerun()

    with tab2:
        data = {}

        data["mac_address"] = st.text_input("Mac Address")
        data["air_pressure"] = st.number_input("Air pressure")
        data["temperature"] = st.number_input("Temperature")
        data["humidity"] = st.number_input("Humidity")
        data["pulse"] = st.number_input("Pulse")
        data["latitude"] = st.number_input("Latitude")
        data["longitude"] = st.number_input("Longitude")
        data["activity"] = st.selectbox("Activity", [True, False])
        data["fall"] = st.selectbox("Fall", [True, False])
        data["analyzer_alarm"] = st.selectbox("Analyzer alarm", [True, False])
        data["charge"] = st.slider("Charge", min_value=1, max_value=100)

        date = st.date_input("Date")
        time = st.time_input("Time")

        data["time"] = datetime.combine(date, time).isoformat()

        btn = st.button("Add")

        if btn:
            insertData(data)
