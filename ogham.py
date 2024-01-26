import unicodedata
import pandas as pd
import streamlit as st

tree_meanings = [ 
    {'name': 'beith', 'tree': 'birch', 'start date': 'Dec 24', 'end date': 'Jan 20', 'meanings': ['new beginnings', 'change', 'release', 'rebirth', 'cleansing', 'hope', 'pioneering energy']},
    {'name': 'luis', 'tree': 'rowan', 'start date': 'Jan 21', 'end date': 'Feb 17', 'meanings': ['insight', 'protection', 'blessings', 'psychic intuition', 'fiery energy', 'perserverance', 'humility']},
    {'name': 'fearn', 'tree': 'alder', 'start date': 'Mar 18', 'end date': 'Apr 14', 'meanings': ['confidence', 'encouragement', 'shield', 'honorable conduct', 'discrimination', 'bad luck', 'secrecy']},
    {'name': 'sail', 'tree': 'willow', 'start date': 'Apr 15', 'end date': 'May 12', 'meanings': ['knowledge', 'spiritual growth', 'moon cycles', "women's cycles", 'April', 'harmony', 'balance', 'grief', 'dreams', 'emotion']},
    {'name': 'nion', 'tree': 'ash', 'start date': 'Feb 18', 'end date': 'Mar 17', 'meanings': ['sacred', 'transitions', 'creativity', 'connections', 'courage', 'focus', 'solar energy', 'vitality']},
    {'name': 'uath', 'tree': 'hawthorn', 'start date': 'May 13', 'end date': 'Jun 9', 'meanings': ['cleansing', 'protection', 'defense', 'fertility', 'masculinity', 'love', 'happiness', 'gentleness', 'beauty']},
    {'name': 'dair', 'tree': 'oak', 'start date': 'Jun 10', 'end date': 'Jul 7', 'meanings': ['strength', 'resiliance', 'self-confidence', 'leadership', 'trust', 'soverieignty', 'loyalty']},
    {'name': 'tinne', 'tree': 'holly', 'start date': 'Jul 8', 'end date': 'Aug 4', 'meanings': ['immordtality', 'unity', 'courage', 'stability of home', 'empathy', 'boundaries', 'protection']},
    {'name': 'coll', 'tree': 'hazel', 'start date': 'Jul 8', 'end date': 'Aug 4', 'meanings': ['wisdom', 'creativity', 'knowledge', 'divination', 'sacred wells', 'communication']},
    {'name': 'ceirt', 'tree': 'apple', 'start date': 'Aug 5', 'end date': 'Sep 1', 'meanings': ['love', 'faithfulness', 'rebirth', 'prosperity', 'fertility', 'attraction', 'faerie realms', 'youthful enerty']},
    {'name': 'muin', 'tree': 'vine', 'start date': 'Sep 2', 'end date': 'Sept 29', 'meanings': ['prophecy', 'truth speaking', 'inward journey', 'life lessons learned', 'harvest', 'wealth', 'cycles']},
    {'name': 'gort', 'tree': 'ivy', 'start date': 'Sep 30', 'end date': 'Oct 27', 'meanings': ['growth', 'wildness', "women's good fortune", 'mystical development', 'protective magic', 'good fortune', 'steadfastness', 'friendship', 'connections', 'support']},
    {'name': 'ngeadal', 'tree': 'reed', 'start date': 'Oct 28', 'end date': 'Nov 24', 'meanings': ['music', 'direct action', 'finding purpose', 'healing', 'health', 'social gathering', 'responsibility', 'ancestral skills', 'order to chaos']},
    {'name': 'straif', 'tree': 'blackthorn', 'start date': 'Oct 28', 'end date': 'Nov 24', 'meanings': ['authority', 'control', 'triumph', 'power', 'anger', 'magical protection', 'banishing negativity']},
    {'name': 'ruis', 'tree': 'elder', 'start date': 'Nov 25', 'end date': 'Dec 23', 'meanings': ['endings', 'maturity', 'wisdom', 'polarity', 'equilibrium', 'purification', 'initiation to dark mysteries', 'underworld goddess work']},
    {'name': 'ailm', 'tree': 'elm', 'meanings': ['clarity', 'alignment', 'perspective', 'calm', 'contemplation', 'meditation']},
    {'name': 'onn', 'tree': 'gorse', 'meanings': ['long-term planning', 'perserverance', 'hope', 'sexuality', 'financial abundance', 'solar energy', 'life force']},
    {'name': 'ur', 'tree': 'heather', 'meanings': ['passion', 'generosity', 'healing', 'positivity', 'love', 'goddess blessings']},
    {'name': 'eadhadh', 'tree': 'aspen', 'meanings': ['endurance', 'courage', 'strong will', 'success', 'spiritual protection']},
    {'name': 'iodhadh', 'tree': 'yew', 'meanings': ['death', 'endings', 'rebirth', 'ancestral wisdom', 'reincarnation', 'other world journeying']}
]
tree_df = pd.DataFrame.from_dict(tree_meanings)


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
    long_name = long_name.replace('ogham', '').strip()

    # st.write(f"{chr(u)} '{long_name}'")

    if long_name in ('ngeadal', 'straif'):
        english = long_name[:2]
    elif 'mark' in long_name:
        english = None
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
        aicme_name = None

    ogham_set[idx] = {
        'code_point': u,
        'ogham_character': chr(u),
        'english_analog': english,
        'category': category,
        'name': long_name,
        'aicme': aicme_name
    }

    ogham_df = pd.DataFrame.from_dict(ogham_set).T
    ogham_merged = ogham_df.merge(tree_df, how='left', on='name')


def replace_english_letters(input_text):
    output_text = input_text[:]
    output_text = output_text.replace('x', 'gs')
    return output_text

def convert_english_to_ogham(input_text):
    english_list = ogham_df['english_analog'].to_list()
    ogham_list = ogham_df['ogham_character'].to_list()

    output_text = ogham_list[-2]
    for e in input_text:
        if e in english_list:
            output_text += ogham_list[english_list.index(e)]
        else:
            output_text += e
    
    return output_text


st.dataframe(ogham_df)

for letter in ogham_set.values():
    st.button(f"{letter['ogham_character']} - {letter['name']}")    

my_name = 'rix'
st.write(f"{my_name} --> {replace_english_letters(my_name)} --> {convert_english_to_ogham(replace_english_letters(my_name))}")

st.dataframe(tree_df)
st.dataframe(ogham_merged)
