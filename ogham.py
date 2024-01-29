# 3rd Party Imports
import pandas as pd
import streamlit as st
from streamlit import session_state as ss


# Built-in Imports
import unicodedata


# Local Imports
from ogham_data import ogham_data


# Data Preparation
ogham_df = pd.DataFrame(ogham_data)


# Initialize Session State
if 'menu_selection' not in ss:
    ss['menu_selection'] = 'Alphabet'


# Callbacks
def callback_basic(old, new=None):
    if new:
        ss[old] = ss[new]
    else:
        ss[old] = ss[f"{old}_new"]


# Local Functions
def strip_accents(text):
    normalized_text = unicodedata.normalize('NFD', text)
    re_encoded_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return str(re_encoded_text)


def convert(english_text):
    english_text = strip_accents(english_text)
    english_text = english_text.replace(' ', '  ')  # double the spaces to make the ogham words stand out
    english_text = english_text.lower()
    ogham_text = '᚛'
    for letter in english_text:
        if letter == ':':
            ogham_letter += ": ᚛"
        else:
            try:
                ogham_letter = ogham_df.loc[ogham_df['english_analog'].str.contains(letter, na=False), 'ogham_character'].values[0]
            except:
                ogham_letter = "?"
        ogham_text += ogham_letter
    return ogham_text


with st.sidebar:
    st.header("Ogham")
    st.selectbox(
        label='Menu',
        options=('Alphabet', 'Quiz', 'Data'),
        key='menu_selection_new',
        on_change=callback_basic,
        kwargs={'old': 'menu_selection'}
    )

st.title(ss['menu_selection'])

if ss['menu_selection'] == 'Alphabet':

    aicmes = ogham_df['aicme'].unique()
    aicmes = [a for a in aicmes if a != None]

    for aicme_name in aicmes:
        alphabet_header_1, alphabet_header_2 = st.columns(2)
        aicme_header_english = f"Aicme {aicme_name}"
        aicme_header_ogham = convert(aicme_header_english)
        alphabet_header_1.header(aicme_header_english)
        alphabet_header_2.header(aicme_header_ogham)

        ogham_letters = ogham_df.loc[ogham_df.aicme == aicme_name, ['ogham_character', 'ogham_name', 'english_analog', 'tree', 'meanings']]
        for ogham_letter in ogham_letters.itertuples():

            alphabet_col_1, alphabet_col_2 = st.columns(2)
            
            # letter_cols = st.columns((1, 1, 1, 5))
            # letter_cols[0].subheader(ogham_letter[1])
            # letter_cols[1].markdown(f'<h3 style="transform-origin: 25% 25%; transform: rotate(-90deg);">{ogham_letter[1]}</style>', unsafe_allow_html=True)
            # letter_cols[2].markdown(f'<h3 style="transform-origin: 0 0; transform: rotate(-90deg);">{ogham_letter[1]}</style>', unsafe_allow_html=True)
            
            alphabet_col_1.subheader(ogham_letter[1])
            alphabet_col_2.subheader(ogham_letter[1])

            name_text = f"Name: {ogham_letter[2]}"
            alphabet_col_1.write(name_text)
            alphabet_col_2.write(convert(name_text))

            alphabet_col_1.write(f"English Alphabet Equivalent: {ogham_letter[3].upper()}")
            alphabet_col_2.write(f"{convert('English Alphabet Equivalent')}: {ogham_letter[3].upper()}")
            
            tree_text = f"Tree Association: {ogham_letter[4]}"
            alphabet_col_1.write(tree_text)
            alphabet_col_2.write(convert(tree_text))

            if ogham_letter[5]:
                meaning_text = f"Meanings: {', '.join(ogham_letter[5])}"
            else:
                meaning_text = "Meanings: only available for the other aicmes"
            alphabet_col_1.write(meaning_text)
            alphabet_col_2.write(convert(meaning_text))

            st.divider()            


elif ss['menu_selection'] == 'Data':
    if st.checkbox("Show Session State"):
        st.write(ss)
    st.dataframe(ogham_df.loc[ogham_df['english_analog'].str.contains('w', na=False), ['ogham_character', 'english_analog']])
    st.dataframe(ogham_df)

elif ss['menu_selection'] == 'Quiz':
    st.selectbox(
        label="Quiz Type",
        options=("Character recognition", "tree meaning", 'name recognition', 'transliteration')
    )

else:
    st.write("Something went wrong")
    st.write(ss)