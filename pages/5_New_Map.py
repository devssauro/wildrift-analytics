import uuid
import streamlit as st
from queries import teams_df, players_df, champion_df, engine

st.set_page_config(
    page_title="Home",
    page_icon="👋",
    layout="wide"
)
st.title("Register new scrim")

side, picks_bans, draft, map_stats = st.tabs(["Side", "Picks & Bans", "Draft", "Map Stats"])

# map_data = {
#     "blue_side_tag": "FLA",
#     "blue_baron_player": "Disturbia",
#     "blue_jungle_player": "Nagata",
#     "blue_mid_player": "Elora",
#     "blue_dragon_player": "Snow",
#     "blue_sup_player": "Lisa",
#     "red_side_tag": "SCAL",
#     "red_baron_player": "Laser",
#     "red_jungle_player": "Rzz",
#     "red_mid_player": "7zinn",
#     "red_dragon_player": "Mathsu",
#     "red_sup_player": "Pilo",
#     "blue_ban_1": [
#     "Olaf"
#     ],
#     "blue_ban_2": [
#     "Lux"
#     ],
#     "blue_ban_3": [
#     "Rengar"
#     ],
#     "blue_ban_4": [
#     "Lee Sin"
#     ],
#     "blue_ban_5": [
#     "Ahri"
#     ],
#     "blue_pick_1": [
#     "Lucian"
#     ],
#     "blue_pick_2": [
#     "Nami"
#     ],
#     "blue_pick_3": [
#     "Kha'Zix"
#     ],
#     "blue_pick_4": [
#     "Ziggs"
#     ],
#     "blue_pick_5": [
#     "Shen"
#     ],
#     "red_pick_1": [
#     "Camille"
#     ],
#     "red_pick_2": [
#     "Corki"
#     ],
#     "red_pick_3": [
#     "Janna"
#     ],
#     "red_pick_4": [
#     "Singed"
#     ],
#     "red_pick_5": [
#     "Jax"
#     ],
#     "red_ban_1": [
#     "Yuumi"
#     ],
#     "red_ban_2": [
#     "Senna"
#     ],
#     "red_ban_3": [
#     "Karma"
#     ],
#     "red_ban_4": [
#     "Seraphine"
#     ],
#     "red_ban_5": [
#     "Wukong"
#     ],
#     "blue_baron_pick": "Shen",
#     "blue_jungle_pick": "Kha'Zix",
#     "blue_mid_pick": "Ziggs",
#     "blue_dragon_pick": "Lucian",
#     "blue_sup_pick": "Nami",
#     "red_baron_pick": "Jax",
#     "red_jungle_pick": "Camille",
#     "red_mid_pick": "Singed",
#     "red_dragon_pick": "Corki",
#     "red_sup_pick": "Janna",
#     "patch": "3.3",
#     "duration": "",
#     "winner": "FLA",
#     "map_number": "1",
#     "blue_baron_kda": "1/3/7",
#     "blue_jungle_kda": "5/2/2",
#     "blue_mid_kda": "0/3/6",
#     "blue_dragon_kda": "2/4/2",
#     "blue_sup_kda": "0/3/7",
#     "red_baron_kda": "4/1/4",
#     "red_jungle_kda": "6/1/5",
#     "red_mid_kda": "0/1/10",
#     "red_dragon_kda": "3/2/8",
#     "red_sup_kda": "2/3/9",
#     "blue_jungle_dmg_dealt": "16097",
#     "blue_mid_dmg_dealt": "18598",
#     "blue_dragon_dmg_dealt": "17495",
#     "blue_sup_dmg_dealt": "7465",
#     "blue_baron_dmg_taken": "4542",
#     "blue_jungle_dmg_taken": "3120",
#     "blue_mid_dmg_taken": "2000",
#     "blue_dragon_dmg_taken": "2743",
#     "blue_sup_dmg_taken": "1806",
#     "blue_baron_total_gold": "9629",
#     "blue_jungle_total_gold": "13156",
#     "blue_mid_total_gold": "11702",
#     "blue_dragon_total_gold": "11619",
#     "blue_sup_total_gold": "8447",
#     "red_baron_dmg_dealt": "12763",
#     "red_jungle_dmg_dealt": "13400",
#     "red_mid_dmg_dealt": "10299",
#     "red_dragon_dmg_dealt": "12978",
#     "red_sup_dmg_dealt": "7025",
#     "red_baron_dmg_taken": "8172",
#     "red_jungle_dmg_taken": "7082",
#     "red_mid_dmg_taken": "7817",
#     "red_dragon_dmg_taken": "4296",
#     "red_sup_dmg_taken": "2394",
#     "red_baron_total_gold": "13013",
#     "red_jungle_total_gold": "13397",
#     "red_mid_total_gold": "11304",
#     "red_dragon_total_gold": "13108",
#     "red_sup_total_gold": "9046"
# }
map_data = {}
uid = str(uuid.uuid4())
match_stats_columns = [
    "tournament", "team_name", "team_tag", "phase", "patch", "matchup_id",
    "map_id", "map_number", "side", "length", "length_sec", "winner", "winner_side",
    "ban_1", "ban_2", "ban_3", "ban_4", "ban_5",
    "pick_1", "pick_2", "pick_3", "pick_4", "pick_5",
    "baron_pick", "jungle_pick", "mid_pick", "dragon_pick", "sup_pick",
    "baron_player", "jungle_player", "mid_player", "dragon_player", "sup_player",
    "baron_kills", "baron_deaths", "baron_assists", "baron_dmg_taken", "baron_dmg_dealt", "baron_total_gold",
    "jungle_kills", "jungle_deaths", "jungle_assists", "jungle_dmg_taken", "jungle_dmg_dealt", "jungle_total_gold",
    "mid_kills", "mid_deaths", "mid_assists", "mid_dmg_taken", "mid_dmg_dealt", "mid_total_gold",
    "dragon_kills", "dragon_deaths", "dragon_assists", "dragon_dmg_taken", "dragon_dmg_dealt", "dragon_total_gold",
    "sup_kills", "sup_deaths", "sup_assists", "sup_dmg_taken", "sup_dmg_dealt", "sup_total_gold"
]

def format_official():
    # _map_data = {**map_data, "tournament": "scrim", "id": uid}

    _map_data = {
        "tournament": "scrim", "id": uid,
        "blue_side_tag": "FLA",
        "blue_baron_player": "Disturbia",
        "blue_jungle_player": "Nagata",
        "blue_mid_player": "Elora",
        "blue_dragon_player": "Snow",
        "blue_sup_player": "Lisa",
        "red_side_tag": "SCAL",
        "red_baron_player": "Laser",
        "red_jungle_player": "Rzz",
        "red_mid_player": "7zinn",
        "red_dragon_player": "Mathsu",
        "red_sup_player": "Pilo",
        "blue_ban_1": [
            "Olaf"
        ],
        "blue_ban_2": [
            "Lux"
        ],
        "blue_ban_3": [
            "Rengar"
        ],
        "blue_ban_4": [
            "Lee Sin"
        ],
        "blue_ban_5": [
            "Ahri"
        ],
        "blue_pick_1": [
            "Lucian"
        ],
        "blue_pick_2": [
            "Nami"
        ],
        "blue_pick_3": [
            "Kha'Zix"
        ],
        "blue_pick_4": [
            "Ziggs"
        ],
        "blue_pick_5": [
            "Shen"
        ],
        "red_pick_1": [
            "Camille"
        ],
        "red_pick_2": [
            "Corki"
        ],
        "red_pick_3": [
            "Janna"
        ],
        "red_pick_4": [
            "Singed"
        ],
        "red_pick_5": [
            "Jax"
        ],
        "red_ban_1": [
            "Yuumi"
        ],
        "red_ban_2": [
            "Senna"
        ],
        "red_ban_3": [
            "Karma"
        ],
        "red_ban_4": [
            "Seraphine"
        ],
        "red_ban_5": [
            "Wukong"
        ],
        "blue_baron_pick": "Shen",
        "blue_jungle_pick": "Kha'Zix",
        "blue_mid_pick": "Ziggs",
        "blue_dragon_pick": "Lucian",
        "blue_sup_pick": "Nami",
        "red_baron_pick": "Jax",
        "red_jungle_pick": "Camille",
        "red_mid_pick": "Singed",
        "red_dragon_pick": "Corki",
        "red_sup_pick": "Janna",
        "patch": "3.3",
        "length": "16:12",
        "winner": "FLA",
        "map_number": "1",
        "blue_baron_kda": "1/3/7",
        "blue_jungle_kda": "5/2/2",
        "blue_mid_kda": "0/3/6",
        "blue_dragon_kda": "2/4/2",
        "blue_sup_kda": "0/3/7",
        "red_baron_kda": "4/1/4",
        "red_jungle_kda": "6/1/5",
        "red_mid_kda": "0/1/10",
        "red_dragon_kda": "3/2/8",
        "red_sup_kda": "2/3/9",
        "blue_baron_dmg_dealt": "8952",
        "blue_jungle_dmg_dealt": "16097",
        "blue_mid_dmg_dealt": "18598",
        "blue_dragon_dmg_dealt": "17495",
        "blue_sup_dmg_dealt": "7465",
        "blue_baron_dmg_taken": "4542",
        "blue_jungle_dmg_taken": "3120",
        "blue_mid_dmg_taken": "2000",
        "blue_dragon_dmg_taken": "2743",
        "blue_sup_dmg_taken": "1806",
        "blue_baron_total_gold": "9629",
        "blue_jungle_total_gold": "13156",
        "blue_mid_total_gold": "11702",
        "blue_dragon_total_gold": "11619",
        "blue_sup_total_gold": "8447",
        "red_baron_dmg_dealt": "12763",
        "red_jungle_dmg_dealt": "13400",
        "red_mid_dmg_dealt": "10299",
        "red_dragon_dmg_dealt": "12978",
        "red_sup_dmg_dealt": "7025",
        "red_baron_dmg_taken": "8172",
        "red_jungle_dmg_taken": "7082",
        "red_mid_dmg_taken": "7817",
        "red_dragon_dmg_taken": "4296",
        "red_sup_dmg_taken": "2394",
        "red_baron_total_gold": "13013",
        "red_jungle_total_gold": "13397",
        "red_mid_total_gold": "11304",
        "red_dragon_total_gold": "13108",
        "red_sup_total_gold": "9046"
    }
    sides = ('blue', 'red')
    roles = ('baron', 'jungle', 'mid', 'dragon', 'sup')
    props = ('dmg_taken', 'dmg_dealt', 'total_gold')
    for side in sides:
        for role in roles:
            for prop in props:
                _map_data[f'{side}_{role}_{prop}'] = int(_map_data[f'{side}_{role}_{prop}'])
            k, d, a = _map_data[f'{side}_{role}_kda'].split('/')
            _map_data[f'{side}_{role}_kills'] = int(k)
            _map_data[f'{side}_{role}_deaths'] = int(d)
            _map_data[f'{side}_{role}_assists'] = int(a)
            del _map_data[f'{side}_{role}_kda']
        for n in range(1, 6):
            _map_data[f'{side}_pick_{n}'] = _map_data[f'{side}_pick_{n}'][0]
            _map_data[f'{side}_ban_{n}'] = None if len(_map_data[f'{side}_ban_{n}']) == 0 \
                else _map_data[f'{side}_ban_{n}'][0]
    _map_data['winner_side'] = 'blue' if _map_data['blue_side_tag'] == _map_data['winner'] else 'red'
    _map_data['blue_side_team'] = teams_df[teams_df.tag == _map_data['blue_side_tag']].name.iloc[0]
    _map_data['red_side_team'] = teams_df[teams_df.tag == _map_data['red_side_tag']].name.iloc[0]
    _map_data['length'] = _map_data['length']
    _length_sec = _map_data['length'].split(':')
    _map_data['length_sec'] = (int(_length_sec[0]) * 60) + int(_length_sec[1])
    del _map_data['length']
    connection = engine.connect()
    connection.execute(f"""
        INSERT INTO maps ({", ".join(_map_data.keys())}) 
        VALUES("{'", "'.join([str(_map_data[c]) for c in _map_data.keys()])}")
    """)



with side:
    blue_side, red_side = st.columns(2)
    with blue_side:
        map_data['blue_side_tag'] = st.selectbox('Blue Side Team', teams_df['tag'])
        blue_players = players_df.query(f'team == "{map_data["blue_side_tag"]}"')
        map_data['blue_baron_player'] = st.selectbox('Blue Baron Player', blue_players['nickname'], 0)
        map_data['blue_jungle_player'] = st.selectbox('Blue Jungle Player', blue_players['nickname'], 1)
        map_data['blue_mid_player'] = st.selectbox('Blue Mid Player', blue_players['nickname'], 2)
        map_data['blue_dragon_player'] = st.selectbox('Blue Dragon Player', blue_players['nickname'], 3)
        map_data['blue_sup_player'] = st.selectbox('Blue Sup Player', blue_players['nickname'], 4)
    with red_side:
        map_data['red_side_tag'] = st.selectbox('Red Side Team',
                                                [t for t in teams_df['tag'] if t != map_data['blue_side_tag']])
        red_players = players_df.query(f'team == "{map_data["red_side_tag"]}"')
        map_data['red_baron_player'] = st.selectbox('Red Baron Player', red_players['nickname'], 0)
        map_data['red_jungle_player'] = st.selectbox('Red Jungle Player', red_players['nickname'], 1)
        map_data['red_mid_player'] = st.selectbox('Red Mid Player', red_players['nickname'], 2)
        map_data['red_dragon_player'] = st.selectbox('Red Dragon Player', red_players['nickname'], 3)
        map_data['red_sup_player'] = st.selectbox('Red Sup Player', red_players['nickname'], 4)
        map_data = map_data

with picks_bans:
    blue_bans, blue_picks, red_picks, red_bans = st.columns(4)

    with blue_bans:
        map_data['blue_ban_1'] = st.multiselect('Blue Ban 1', champion_df['name'])
        map_data['blue_ban_2'] = st.multiselect(
            'Blue Ban 2', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'))])
        map_data['blue_ban_3'] = st.multiselect(
            'Blue Ban 3', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'))])
        map_data['blue_ban_4'] = st.multiselect(
            'Blue Ban 4', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'), map_data.get('blue_pick_3'),
                map_data.get('red_pick_3'),
                map_data.get('red_ban_4'),
            )])
        map_data['blue_ban_5'] = st.multiselect(
            'Blue Ban 5', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'), map_data.get('blue_pick_3'),
                map_data.get('red_pick_3'),
                map_data.get('red_ban_4'),
                map_data.get('blue_ban_4'),
                map_data.get('red_ban_5'),
            )])
    with blue_picks:
        map_data['blue_pick_1'] = st.multiselect(
            'Blue Pick 1', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3')
            )])
        map_data['blue_pick_2'] = st.multiselect(
            'Blue Pick 2', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
            )])
        map_data['blue_pick_3'] = st.multiselect(
            'Blue Pick 3', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'),
            )])
        map_data['blue_pick_4'] = st.multiselect(
            'Blue Pick 4', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'), map_data.get('blue_pick_3'),
                map_data.get('red_pick_3'),
                map_data.get('red_ban_4'),
                map_data.get('blue_ban_4'),
                map_data.get('red_ban_5'),
                map_data.get('blue_ban_5'),
                map_data.get('red_pick_4'),
            )])
        map_data['blue_pick_5'] = st.multiselect(
            'Blue Pick 5', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'), map_data.get('blue_pick_3'),
                map_data.get('red_pick_3'),
                map_data.get('red_ban_4'),
                map_data.get('blue_ban_4'),
                map_data.get('red_ban_5'),
                map_data.get('blue_ban_5'),
                map_data.get('red_pick_4'),
                map_data.get('blue_pick_4'),
            )])

    with red_picks:
        map_data['red_pick_1'] = st.multiselect(
            'Red Pick 1', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
            )])
        map_data['red_pick_2'] = st.multiselect(
            'Red Pick 2', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
            )])
        map_data['red_pick_3'] = st.multiselect(
            'Red Pick 3', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'), map_data.get('blue_pick_3'),
            )])
        map_data['red_pick_4'] = st.multiselect(
            'Red Pick 4', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'), map_data.get('blue_pick_3'),
                map_data.get('red_pick_3'),
                map_data.get('red_ban_4'),
                map_data.get('blue_ban_4'),
                map_data.get('red_ban_5'),
                map_data.get('blue_ban_5')
            )])
        map_data['red_pick_5'] = st.multiselect(
            'Red Pick 5', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'), map_data.get('blue_pick_3'),
                map_data.get('red_pick_3'),
                map_data.get('red_ban_4'),
                map_data.get('blue_ban_4'),
                map_data.get('red_ban_5'),
                map_data.get('blue_ban_5'),
                map_data.get('red_pick_4'),
                map_data.get('blue_pick_4'), map_data.get('blue_pick_5')
            )])

    with red_bans:
        map_data['red_ban_1'] = st.multiselect(
            'Red Ban 1', [c for c in champion_df['name'] if c not in (
                map_data.get("blue_ban_1")
            )])
        map_data['red_ban_2'] = st.multiselect(
            'Red Ban 2', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'))])
        map_data['red_ban_3'] = st.multiselect(
            'Red Ban 3', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3')
            )])
        map_data['red_ban_4'] = st.multiselect(
            'Red Ban 4', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'), map_data.get('blue_pick_3'),
                map_data.get('red_pick_3'),
            )])
        map_data['red_ban_5'] = st.multiselect(
            'Red Ban 5', [c for c in champion_df['name'] if c not in (
                map_data.get('red_ban_1'), map_data.get('blue_ban_1'),
                map_data.get('red_ban_2'), map_data.get('blue_ban_2'),
                map_data.get('red_ban_3'), map_data.get('blue_ban_3'),
                map_data.get('blue_pick_1'),
                map_data.get('red_pick_1'), map_data.get('red_pick_2'),
                map_data.get('blue_pick_2'), map_data.get('blue_pick_3'),
                map_data.get('red_pick_3'),
                map_data.get('red_ban_4'),
                map_data.get('blue_ban_4'),
            )])

with draft:
    blue_champions = [map_data.get(f'blue_pick_{n}')[0] for n in range(1, 6) if len(map_data.get(f'blue_pick_{n}')) > 0]
    red_champions = [map_data.get(f'red_pick_{n}')[0] for n in range(1, 6) if len(map_data.get(f'red_pick_{n}')) > 0]
    blue_side, red_side = st.columns(2)
    with blue_side:
        map_data['blue_baron_pick'] = st.selectbox('Blue Baron Pick', blue_champions, 0)
        map_data['blue_jungle_pick'] = st.selectbox('Blue Jungle Pick', blue_champions, 1)
        map_data['blue_mid_pick'] = st.selectbox('Blue Mid Pick', blue_champions, 0)
        map_data['blue_dragon_pick'] = st.selectbox('Blue Dragon Pick', blue_champions, 1)
        map_data['blue_sup_pick'] = st.selectbox('Blue Sup Pick', blue_champions, 1)
    with red_side:
        map_data['red_baron_pick'] = st.selectbox('Red Baron Pick', red_champions, 0)
        map_data['red_jungle_pick'] = st.selectbox('Red Jungle Pick', red_champions, 1)
        map_data['red_mid_pick'] = st.selectbox('Red Mid Pick', red_champions, 0)
        map_data['red_dragon_pick'] = st.selectbox('Red Dragon Pick', red_champions, 1)
        map_data['red_sup_pick'] = st.selectbox('Red Sup Pick', red_champions, 1)

with map_stats:
    patch, duration, winner, map_number = st.columns(4)
    kda, dmg_gold = st.tabs(['KDA', 'DMG & Gold'])
    map_data['patch'] = patch.text_input('Patch', '3.3')
    map_data['length'] = duration.text_input('Duration')
    map_data['winner'] = winner.selectbox('winner', [map_data['blue_side_tag'], map_data['red_side_tag']])
    map_data['map_number'] = map_number.text_input('Map Number', 1)
    with kda:
        blue_side, red_side = st.columns(2)
        map_data['blue_baron_kda'] = blue_side.text_input('Blue Baron KDA')
        map_data['blue_jungle_kda'] = blue_side.text_input('Blue Jungle KDA')
        map_data['blue_mid_kda'] = blue_side.text_input('Blue Mid KDA')
        map_data['blue_dragon_kda'] = blue_side.text_input('Blue Dragon KDA')
        map_data['blue_sup_kda'] = blue_side.text_input('Blue Sup KDA')
        map_data['red_baron_kda'] = red_side.text_input('Red Baron KDA')
        map_data['red_jungle_kda'] = red_side.text_input('Red Jungle KDA')
        map_data['red_mid_kda'] = red_side.text_input('Red Mid KDA')
        map_data['red_dragon_kda'] = red_side.text_input('Red Dragon KDA')
        map_data['red_sup_kda'] = red_side.text_input('Red Sup KDA')
    with dmg_gold:
        blue_dmg_dealt, blue_dmg_taken, blue_gold, red_dmg_dealt, red_dmg_taken, red_gold = st.columns(6)
        with blue_dmg_dealt:
            map_data['blue_baron_dmg_dealt'] = st.text_input('Blue Baron DMG Dealt')
            map_data['blue_jungle_dmg_dealt'] = st.text_input('Blue Jungle DMG Dealt')
            map_data['blue_mid_dmg_dealt'] = st.text_input('Blue Mid DMG Dealt')
            map_data['blue_dragon_dmg_dealt'] = st.text_input('Blue Dragon DMG Dealt')
            map_data['blue_sup_dmg_dealt'] = st.text_input('Blue Sup DMG Dealt')
        with blue_dmg_taken:
            map_data['blue_baron_dmg_taken'] = st.text_input('Blue Baron DMG Taken')
            map_data['blue_jungle_dmg_taken'] = st.text_input('Blue Jungle DMG Taken')
            map_data['blue_mid_dmg_taken'] = st.text_input('Blue Mid DMG Taken')
            map_data['blue_dragon_dmg_taken'] = st.text_input('Blue Dragon DMG Taken')
            map_data['blue_sup_dmg_taken'] = st.text_input('Blue Sup DMG Taken')
        with blue_gold:
            map_data['blue_baron_total_gold'] = st.text_input('Blue Baron Gold')
            map_data['blue_jungle_total_gold'] = st.text_input('Blue Jungle Gold')
            map_data['blue_mid_total_gold'] = st.text_input('Blue Mid Gold')
            map_data['blue_dragon_total_gold'] = st.text_input('Blue Dragon Gold')
            map_data['blue_sup_total_gold'] = st.text_input('Blue Sup Gold')
        with red_dmg_dealt:
            map_data['red_baron_dmg_dealt'] = st.text_input('Red Baron DMG Dealt')
            map_data['red_jungle_dmg_dealt'] = st.text_input('Red Jungle DMG Dealt')
            map_data['red_mid_dmg_dealt'] = st.text_input('Red Mid DMG Dealt')
            map_data['red_dragon_dmg_dealt'] = st.text_input('Red Dragon DMG Dealt')
            map_data['red_sup_dmg_dealt'] = st.text_input('Red Sup DMG Dealt')
        with red_dmg_taken:
            map_data['red_baron_dmg_taken'] = st.text_input('Red Baron DMG Taken')
            map_data['red_jungle_dmg_taken'] = st.text_input('Red Jungle DMG Taken')
            map_data['red_mid_dmg_taken'] = st.text_input('Red Mid DMG Taken')
            map_data['red_dragon_dmg_taken'] = st.text_input('Red Dragon DMG Taken')
            map_data['red_sup_dmg_taken'] = st.text_input('Red Sup DMG Taken')
        with red_gold:
            map_data['red_baron_total_gold'] = st.text_input('Red Baron Gold')
            map_data['red_jungle_total_gold'] = st.text_input('Red Jungle Gold')
            map_data['red_mid_total_gold'] = st.text_input('Red Mid Gold')
            map_data['red_dragon_total_gold'] = st.text_input('Red Dragon Gold')
            map_data['red_sup_total_gold'] = st.text_input('Red Sup Gold')
# st.write(map_data)
st.button("Save", on_click=format_official)
