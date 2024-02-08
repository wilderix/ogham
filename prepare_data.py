import json
import pandas as pd
import pyperclip
import streamlit as st
import unicodedata
from ogham_data import ogham_data


for od, row in enumerate(ogham_data):
    cp = row['code_point']
    print(f"code_point: {cp}, unicode_name: {unicodedata.name(chr(cp))}")
    ogham_data[od]['unicode_name'] = unicodedata.name(chr(cp))

ogham_df = pd.DataFrame(ogham_data)

column_names = list(ogham_df.columns)
column_names.sort()


st.title("Ogham Data")
st.dataframe(ogham_df.loc[:, column_names])

# jd = json.dumps(ogham_data)
# pyperclip.copy(jd)
