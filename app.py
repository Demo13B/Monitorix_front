import streamlit as st
import json
import pandas as pd

st.title("Test app")

json_string = '''[{"name":"Tim", "gender":"male"}, {"name":"Bertha", "gender":"female"}]'''
json_object = json.loads(json_string)

df = pd.DataFrame(json_object)

st.dataframe(df, hide_index=True)
