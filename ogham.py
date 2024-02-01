# 3rd Party Imports
import pandas as pd
import streamlit as st
from streamlit import session_state as ss


# Built-in Imports
import unicodedata


# Local Imports
from ogham_data import ogham_data, kennings


# Data Preparation
ogham_df = pd.DataFrame(ogham_data)
kennings_df = pd.DataFrame(kennings)


# Initialize Session State
if 'menu_selection' not in ss:
    ss['menu_selection'] = 'Alphabet'
if 'aicme_stroke' not in ss:
    ss['aicme_stroke'] = ''
if 'aicme_stroke_conversion' not in ss:
    ss['aicme_stroke_conversion'] = ''


# Callbacks
def callback_basic(old, new=None):
    if new:
        ss[old] = ss[new]
    else:
        ss[old] = ss[f"{old}_new"]

def callback_aicme_stroke(old, new=None):
    callback_basic(old)
    aicme_initials = 'bhmaf'
    text_list = ss['aicme_stroke'][:].split()
    n = 2
    # pairs = [ss['aicme_stroke'][i:i+n] for i in range(0, len(ss['aicme_stroke']), n)]
    output_list = []
    for text in text_list:
        output_text = ''
        pairs = [text[i:i+n] for i in range(0, len(text), n)]
        for pair in pairs:
            if pair[0] == 'b':
                aicme = 'Beithe'
            elif pair[0] == 'h':
                aicme = 'hÚatha'
            elif pair[0] == 'm':
                aicme = 'Muine'
            elif pair[0] == 'a':
                aicme = 'Ailme'
            elif pair[0] == 'f':
                aicme = 'Forfeda'

            if pair[0] not in aicme_initials and pair[1] not in '12345':
                st.warning("Get it right")
            else:
                ogham_letter = ogham_df.loc[
                    (ogham_df['aicme'] == aicme) &
                    (ogham_df['aicme_position'] == int(pair[1])),
                    ['ogham_character']
                ].iloc[0, 0]
            output_text += ogham_letter
        output_list.append(output_text)
    ss['aicme_stroke_conversion'] = output_list

# Local Functions
def strip_accents(text):
    normalized_text = unicodedata.normalize('NFD', text)
    re_encoded_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return str(re_encoded_text)


def convert(english_text):
    english_text = strip_accents(english_text)
    # english_text = english_text.replace(' ', '  ')  # double the spaces to make the ogham words stand out
    english_text = english_text.lower()
    ogham_text = '᚛'
    for letter in english_text:
        if letter == ':':
            ogham_letter = " ᚛"
        elif letter == ',':
            ogham_letter = "᚜ ᚛"
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
        options=('Alphabet', 'Quiz', 'Data', 'Aicmes', 'Write'),
        key='menu_selection_new',
        on_change=callback_basic,
        kwargs={'old': 'menu_selection'}
    )
    if st.checkbox("Show Sessioin State"):
        ss


st.title(ss['menu_selection'])


if ss['menu_selection'] == 'Aicmes':

    # Beithe, hÚatha, Muine, Ailme, Forfeda, Punctuation

    chars, names, english, trees = st.tabs(('Ogham Characters', 'Ogham Names', 'English Letters', 'Tree Correspondence'))
    chars.dataframe(
        ogham_df.pivot(index='aicme_position', columns='aicme', values='ogham_character'),
        hide_index=True,
        column_order=('Beithe', 'hÚatha', 'Muine', 'Ailme', 'Forfeda', 'Punctuation')
    )
    names.dataframe(ogham_df.pivot(index='aicme_position', columns='aicme', values='ogham_name'),
        hide_index=True,
        column_order=('Beithe', 'hÚatha', 'Muine', 'Ailme',  'Forfeda', 'Punctuation')
    )
    english.dataframe(ogham_df.pivot(index='aicme_position', columns='aicme', values='english_analog'),
        hide_index=True,
        column_order=('Beithe', 'hÚatha', 'Muine', 'Ailme',  'Forfeda', 'Punctuation')
    )
    trees.dataframe(ogham_df.pivot(index='aicme_position', columns='aicme', values='tree'),
        hide_index=True,
        column_order=('Beithe', 'hÚatha', 'Muine', 'Ailme',  'Forfeda', 'Punctuation')
    )


elif ss['menu_selection'] == 'Alphabet':

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

            alphabet_col_1.write(f"English Alphabet Equivalent: {ogham_letter[3]}")
            alphabet_col_2.write(f"{convert('English Alphabet Equivalent')} {ogham_letter[3]}")
            
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
    st.dataframe(kennings_df)


elif ss['menu_selection'] == 'Write':
    pass
    st.text_input(
        label="Enter text here",
        key='aicme_stroke_new',
        on_change=callback_aicme_stroke,
        kwargs={'old': 'aicme_stroke'}
    )
    for word in ss['aicme_stroke_conversion']:
        st.write(word)


elif ss['menu_selection'] == 'Quiz':
    st.selectbox(
        label="Quiz Type",
        options=("Character recognition", "tree meaning", 'name recognition', 'transliteration')
    )



else:
    st.write("Something went wrong")
    st.write(ss)