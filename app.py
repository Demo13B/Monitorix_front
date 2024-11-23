import streamlit as st

st.title("Test app")

name = st.text_input("What is your name?")

if st.button("Submit"):
    st.write(f"Hello, {name}!")
