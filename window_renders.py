import streamlit as st
import seaborn as sns  # type: ignore
import matplotlib.pyplot as plt
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


def render_users_page():
    st.title("Users")

    queryUsers()

    st.dataframe(st.session_state.users_df, hide_index=True)


def render_data_page():
    st.title("Data")

    queryData()

    st.dataframe(st.session_state.data_df, hide_index=True)


def render_alerts_page():
    st.title("Alerts")

    queryAlerts()

    st.dataframe(st.session_state.alerts_df, hide_index=True)


def render_brigades_page():
    st.title("Brigades")

    queryBrigades()

    st.dataframe(st.session_state.brigades_df, hide_index=True)


def render_facilities_page():
    st.title("Facilities")

    queryFacilities()

    st.dataframe(st.session_state.facilities_df, hide_index=True)


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
