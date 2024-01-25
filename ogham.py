import unicodedata
import pandas as pd
import streamlit as st




start, end = 5760, 5788
ogham_set = {}
aicme_idx = None

aicmes = ['Beithe', 'hÚatha', 'Muine', 'Ailme', 'Forfeda']
aicme_markers = []
for a, name in enumerate(aicmes):
    marker = a * 5
    marker += start
    marker += 1
    aicme_markers.append(marker)

for u in range(start, end+1):
    idx = u - 5760
    category = unicodedata.category(chr(u))
    long_name = unicodedata.name(chr(u))
    long_name = long_name.replace('OGHAM LETTER', '').lower().strip()

    # st.write(f"{chr(u)} '{long_name}'")

    if long_name in ('ngeadal', 'straif'):
        english = long_name[:2]
    elif 'mark' in long_name:
        english = ''
    elif long_name == 'fearn':
        english = 'w'
    elif long_name == 'uath':
        english = 'h'
    elif long_name == 'ceirt':
        english = 'q'
    else:
        english = long_name[0]

    if u in aicme_markers and category == 'Lo':
        aicme_idx = aicme_markers.index(u)
        aicme_name = aicmes[aicme_idx]
    elif category != 'Lo':
        aicme_name = 'punctuation'

    ogham_set[idx] = {
        'code_point': u,
        'char': chr(u),
        'english': english,
        'category': category,
        'name': long_name,
        'aicme': aicme_name
    }
    ogham_df = pd.DataFrame.from_dict(ogham_set).T


def replace_english_letters(input_text):
    output_text = input_text[:]
    output_text = output_text.replace('x', 'gs')
    return output_text

def convert_english_to_ogham(input_text):
    english_list = ogham_df['english'].to_list()
    ogham_list = ogham_df['char'].to_list()

    output_text = ogham_list[-2]
    for e in input_text:
        if e in english_list:
            output_text += ogham_list[english_list.index(e)]
        else:
            output_text += e
    
    return output_text


st.dataframe(pd.DataFrame.from_dict(ogham_set).T)

for letter in ogham_set.values():
    st.button(f"{letter['char']} - {letter['name']}")    

my_name = 'rix'
st.write(f"{my_name} --> {replace_english_letters(my_name)} --> {convert_english_to_ogham(replace_english_letters(my_name))}")