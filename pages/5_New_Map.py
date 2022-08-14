import uuid
import streamlit as st
import pandas as pd
from queries import client
from sqlalchemy import create_engine
# from models import Session
from queries import credentials

st.set_page_config(
    page_title="Home",
    page_icon="👋",
    layout="wide"
)
st.title("Register new scrim")
uid = str(uuid.uuid4())

engine = create_engine(
    "gsheets://",
    service_account_info=st.secrets['gcp_service_account'],
    catalog={
        'teams': f'{st.secrets["private_gsheets_url"]}&gid={st.secrets["teams_sheet"]}&headers=1',
        'players': f'{st.secrets["private_gsheets_url"]}&gid={st.secrets["players_sheet"]}&headers=1',
        'champions': f'{st.secrets["private_gsheets_url"]}&gid={st.secrets["champions_sheet"]}&headers=1',
        'tournaments': f'{st.secrets["private_gsheets_url"]}&gid={st.secrets["tournaments_sheet"]}&headers=1',
    }
)


@st.cache(ttl=300)
def load_data():
    return pd.read_sql(
        'SELECT * FROM champions',
        con=engine.raw_connection()
    ), pd.read_sql(
        'SELECT * FROM teams WHERE tag IS NOT NULL',
        con=engine.raw_connection()
    ), pd.read_sql(
        'SELECT * FROM players WHERE nickname IS NOT NULL',
        con=engine.raw_connection()
    ), pd.read_sql(
        'SELECT * FROM tournaments WHERE name IS NOT NULL',
        con=engine.raw_connection()
    )


champion_df, teams_df, players_df, tournaments_df = load_data()

qtd_games, matchup_id, tournament = st.columns(3)

mdn = qtd_games.number_input('Qty Games', 1)
_uid = matchup_id.text_input('Matchup ID', uid, disabled=True)
_tnmt = tournament.selectbox('Tournament', tournaments_df.name)

maps = []
# map_data = {}
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
    sides = ('blue', 'red')
    roles = ('baron', 'jungle', 'mid', 'dragon', 'sup')
    props = ('dmg_taken', 'dmg_dealt', 'total_gold')
    # session = Session()
    _maps = []
    for map in maps:
        _map_data = {**map, "tournament": _tnmt, "matchup_id": uid, "id": str(uuid.uuid4())}
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
                _map_data[f'{side}_ban_{n}'] = '' if _map_data[f'{side}_ban_{n}'] == 'Nenhum' \
                    else _map_data[f'{side}_ban_{n}']
        _map_data['winner_side'] = 'blue' if _map_data['blue_side_tag'] == _map_data['winner'] else 'red'
        _map_data['blue_side_team'] = teams_df[teams_df.tag == _map_data['blue_side_tag']].name.iloc[0]
        _map_data['red_side_team'] = teams_df[teams_df.tag == _map_data['red_side_tag']].name.iloc[0]
        if _map_data.get('length') not in (None, ''):
            _length_sec = _map_data['length'].split(':')
            _map_data['length_sec'] = (int(_length_sec[0]) * 60) + int(_length_sec[1])
        _maps.append(_map_data)
        # for k in _map_data.keys():
        #     print(f'{k},')
    print(f'adding data: {_maps}')
    load_job = client.load_table_from_json(_maps, 'map_data.maps')
    load_job.result()
    destination_table = client.get_table('map_data.maps')
    print("Loaded {} rows.".format(destination_table.num_rows))


for index in range(int(mdn)):
    st.header(f'Map {index+1}')
    side, picks_bans, draft, map_stats = st.tabs(["Side", "Picks & Bans", "Draft", "Map Stats"])
    map_data = {}
    with side:
        blue_side, red_side = st.columns(2)
        with blue_side:
            map_data['blue_side_tag'] = st.selectbox(
                'Blue Side Team', teams_df['tag'], key=f'blue_side_tag_{index}')
            blue_players = players_df.query(f'team == "{map_data["blue_side_tag"]}"')
            map_data['blue_baron_player'] = st.selectbox(
                'Blue Baron Player', blue_players['nickname'], 0, key=f'blue_baron_player_{index}')
            map_data['blue_jungle_player'] = st.selectbox(
                'Blue Jungle Player', blue_players['nickname'], 1, key=f'blue_jungle_player_{index}')
            map_data['blue_mid_player'] = st.selectbox(
                'Blue Mid Player', blue_players['nickname'], 2, key=f'blue_mid_player_{index}')
            map_data['blue_dragon_player'] = st.selectbox(
                'Blue Dragon Player', blue_players['nickname'], 3, key=f'blue_dragon_player_{index}')
            map_data['blue_sup_player'] = st.selectbox(
                'Blue Sup Player', blue_players['nickname'], 4, key=f'blue_sup_player_{index}')
        with red_side:
            map_data['red_side_tag'] = st.selectbox(
                'Red Side Team', [t for t in teams_df['tag'] if t != map_data['blue_side_tag']],
                key=f'red_side_tag_{index}')
            red_players = players_df.query(f'team == "{map_data["red_side_tag"]}"')
            map_data['red_baron_player'] = st.selectbox(
                'Red Baron Player', red_players['nickname'], 0, key=f'red_baron_player_{index}')
            map_data['red_jungle_player'] = st.selectbox(
                'Red Jungle Player', red_players['nickname'], 1, key=f'red_jungle_player_{index}')
            map_data['red_mid_player'] = st.selectbox(
                'Red Mid Player', red_players['nickname'], 2, key=f'red_mid_player_{index}')
            map_data['red_dragon_player'] = st.selectbox(
                'Red Dragon Player', red_players['nickname'], 3, key=f'red_dragon_player_{index}')
            map_data['red_sup_player'] = st.selectbox(
                'Red Sup Player', red_players['nickname'], 4, key=f'red_sup_player_{index}')
            map_data = map_data

    with picks_bans:
        blue_bans, blue_picks, red_picks, red_bans = st.columns(4)
        map_data['blue_ban_1'] = blue_bans.selectbox(
            'Blue Ban 1', ['Nenhum', *champion_df['name']], 0, key=f'blue_ban_1_{index}')
        map_data['red_ban_1'] = red_bans.selectbox(
            'Red Ban 1', ['Nenhum', *[c for c in champion_df['name'] if c != map_data['blue_ban_1']]], 0, key=f'red_ban_1_{index}')
        map_data['blue_ban_2'] = blue_bans.selectbox(
            'Blue Ban 2', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1']
            )]], 0, key=f'blue_ban_2_{index}')
        map_data['red_ban_2'] = red_bans.selectbox(
            'Red Ban 2', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2']
            )]], 0, key=f'red_ban_2_{index}')
        map_data['blue_ban_3'] = blue_bans.selectbox(
            'Blue Ban 3', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2']
            )]], 0, key=f'blue_ban_3_{index}')
        map_data['red_ban_3'] = red_bans.selectbox(
            'Red Ban 3', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3']
            )]], 0, key=f'red_ban_3_{index}')
        map_data['blue_pick_1'] = blue_picks.selectbox(
            'Blue Pick 1', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3']
            )]], 0, key=f'blue_pick_1_{index}')
        map_data['red_pick_1'] = red_picks.selectbox(
            'Red Pick 1', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1']
            )]], 0, key=f'red_pick_1_{index}')
        map_data['red_pick_2'] = red_picks.selectbox(
            'Red Pick 2', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1']
            )]], 0, key=f'red_pick_2_{index}')
        map_data['blue_pick_2'] = blue_picks.selectbox(
            'Blue Pick 2', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2']
            )]], 0, key=f'blue_pick_2_{index}')
        map_data['blue_pick_3'] = blue_picks.selectbox(
            'Blue Pick 3', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2']
            )]], 0, key=f'blue_pick_3_{index}')
        map_data['red_pick_3'] = red_picks.selectbox(
            'Red Pick 3', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2'],
                map_data['blue_pick_3']
            )]], 0, key=f'red_pick_3_{index}')
        map_data['red_ban_4'] = red_bans.selectbox(
            'Red Ban 4', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2'],
                map_data['blue_pick_3'], map_data['red_pick_3']
            )]], 0, key=f'red_ban_4_{index}')
        map_data['blue_ban_4'] = blue_bans.selectbox(
            'Blue Ban 4', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2'],
                map_data['blue_pick_3'], map_data['red_pick_3'],
                map_data['red_ban_4']
            )]], 0, key=f'blue_ban_4_{index}')
        map_data['red_ban_5'] = red_bans.selectbox(
            'Red Ban 5', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2'],
                map_data['blue_pick_3'], map_data['red_pick_3'],
                map_data['red_ban_4'], map_data['blue_ban_4']
            )]], 0, key=f'red_ban_5_{index}')
        map_data['blue_ban_5'] = blue_bans.selectbox(
            'Blue Ban 5', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2'],
                map_data['blue_pick_3'], map_data['red_pick_3'],
                map_data['red_ban_4'], map_data['blue_ban_4'],
                map_data['red_ban_5']
            )]], 0, key=f'blue_ban_5_{index}')
        map_data['red_pick_4'] = red_picks.selectbox(
            'Red Pick 4', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2'],
                map_data['blue_pick_3'], map_data['red_pick_3'],
                map_data['red_ban_4'], map_data['blue_ban_4'],
                map_data['red_ban_5'], map_data['blue_ban_5']
            )]], 0, key=f'red_ban_4_{index}')
        map_data['blue_pick_4'] = blue_picks.selectbox(
            'Blue Pick 4', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2'],
                map_data['blue_pick_3'], map_data['red_pick_3'],
                map_data['red_ban_4'], map_data['blue_ban_4'],
                map_data['red_ban_5'], map_data['blue_ban_5'],
                map_data['red_pick_4']
            )]], 0, key=f'blue_pick_4_{index}')
        map_data['blue_pick_5'] = blue_picks.selectbox(
            'Blue Pick 5', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2'],
                map_data['blue_pick_3'], map_data['red_pick_3'],
                map_data['red_ban_4'], map_data['blue_ban_4'],
                map_data['red_ban_5'], map_data['blue_ban_5'],
                map_data['red_pick_4'], map_data['blue_pick_4']
            )]], 0, key=f'blue_pick_5_{index}')
        map_data['red_pick_5'] = red_picks.selectbox(
            'Red Pick 5', ['Nenhum', *[c for c in champion_df['name'] if c not in (
                map_data['blue_ban_1'], map_data['red_ban_1'],
                map_data['blue_ban_2'], map_data['red_ban_2'],
                map_data['blue_ban_3'], map_data['red_ban_3'],
                map_data['blue_pick_1'], map_data['red_pick_1'],
                map_data['red_pick_2'], map_data['blue_pick_2'],
                map_data['blue_pick_3'], map_data['red_pick_3'],
                map_data['red_ban_4'], map_data['blue_ban_4'],
                map_data['red_ban_5'], map_data['blue_ban_5'],
                map_data['red_pick_4'], map_data['blue_pick_4'],
                map_data['blue_pick_5']
            )]], 0, key=f'blue_red_5_{index}')

    with draft:
        blue_champions = [map_data.get(f'blue_pick_{n}')
                          for n in range(1, 6) if len(map_data.get(f'blue_pick_{n}')) > 0]
        red_champions = [map_data.get(f'red_pick_{n}')
                         for n in range(1, 6) if len(map_data.get(f'red_pick_{n}')) > 0]
        blue_side, red_side = st.columns(2)

        with blue_side:
            map_data['blue_baron_pick'] = st.selectbox(
                'Blue Baron Pick', blue_champions, 0, key=f'blue_baron_pick_{index}')
            map_data['blue_jungle_pick'] = st.selectbox(
                'Blue Jungle Pick', blue_champions, 1, key=f'blue_jungle_pick_{index}')
            map_data['blue_mid_pick'] = st.selectbox(
                'Blue Mid Pick', blue_champions, 2, key=f'blue_mid_pick_{index}')
            map_data['blue_dragon_pick'] = st.selectbox(
                'Blue Dragon Pick', blue_champions, 3, key=f'blue_dragon_pick_{index}')
            map_data['blue_sup_pick'] = st.selectbox(
                'Blue Sup Pick', blue_champions, 4, key=f'blue_sup_pick_{index}')

        with red_side:
            map_data['red_baron_pick'] = st.selectbox(
                'Red Baron Pick', red_champions, 0, key=f'red_baron_pick_{index}')
            map_data['red_jungle_pick'] = st.selectbox(
                'Red Jungle Pick', red_champions, 1, key=f'red_jungle_pick_{index}')
            map_data['red_mid_pick'] = st.selectbox(
                'Red Mid Pick', red_champions, 2, key=f'red_mid_pick_{index}')
            map_data['red_dragon_pick'] = st.selectbox(
                'Red Dragon Pick', red_champions, 3, key=f'red_dragon_pick_{index}')
            map_data['red_sup_pick'] = st.selectbox(
                'Red Sup Pick', red_champions, 4, key=f'red_sup_pick_{index}')

    with map_stats:
        patch, duration, winner, map_number = st.columns(4)
        kda, dmg_gold = st.tabs(['KDA', 'DMG & Gold'])
        map_data['patch'] = patch.text_input('Patch', '3.3a', key=f'patch_{index}')
        map_data['length'] = duration.text_input('Duration', key=f'length_{index}')
        map_data['winner'] = winner.selectbox(
            'winner', [map_data['blue_side_tag'], map_data['red_side_tag']], key=f'winner_{index}_{str(uuid.uuid4())}')
        map_data['map_number'] = map_number.text_input('Map Number', index+1, key=f'winner_{index}', disabled=True)
        with kda:
            blue_side, red_side = st.columns(2)
            map_data['blue_baron_kda'] = blue_side.text_input('Blue Baron KDA', key=f'blue_baron_kda_{index}')
            map_data['blue_jungle_kda'] = blue_side.text_input('Blue Jungle KDA', key=f'blue_jungle_kda_{index}')
            map_data['blue_mid_kda'] = blue_side.text_input('Blue Mid KDA', key=f'blue_mid_kda_{index}')
            map_data['blue_dragon_kda'] = blue_side.text_input('Blue Dragon KDA', key=f'blue_dragon_kda_{index}')
            map_data['blue_sup_kda'] = blue_side.text_input('Blue Sup KDA', key=f'blue_sup_kda_{index}')
            map_data['red_baron_kda'] = red_side.text_input('Red Baron KDA', key=f'red_baron_kda_{index}')
            map_data['red_jungle_kda'] = red_side.text_input('Red Jungle KDA', key=f'red_jungle_kda_{index}')
            map_data['red_mid_kda'] = red_side.text_input('Red Mid KDA', key=f'red_mid_kda_{index}')
            map_data['red_dragon_kda'] = red_side.text_input('Red Dragon KDA', key=f'red_dragon_kda_{index}')
            map_data['red_sup_kda'] = red_side.text_input('Red Sup KDA', key=f'red_sup_kda_{index}')
        with dmg_gold:
            blue_dmg_dealt, blue_dmg_taken, blue_gold, red_dmg_dealt, red_dmg_taken, red_gold = st.columns(6)
            with blue_dmg_dealt:
                map_data['blue_baron_dmg_dealt'] = st.text_input(
                    'Blue Baron DMG Dealt', key=f'blue_baron_dmg_dealt_{index}')
                map_data['blue_jungle_dmg_dealt'] = st.text_input(
                    'Blue Jungle DMG Dealt', key=f'blue_jungle_dmg_dealt_{index}')
                map_data['blue_mid_dmg_dealt'] = st.text_input(
                    'Blue Mid DMG Dealt', key=f'blue_mid_dmg_dealt_{index}')
                map_data['blue_dragon_dmg_dealt'] = st.text_input(
                    'Blue Dragon DMG Dealt', key=f'blue_dragon_dmg_dealt_{index}')
                map_data['blue_sup_dmg_dealt'] = st.text_input(
                    'Blue Sup DMG Dealt', key=f'blue_sup_dmg_dealt_{index}')
            with blue_dmg_taken:
                map_data['blue_baron_dmg_taken'] = st.text_input(
                    'Blue Baron DMG Taken', key=f'blue_baron_dmg_taken_{index}')
                map_data['blue_jungle_dmg_taken'] = st.text_input(
                    'Blue Jungle DMG Taken', key=f'blue_jungle_dmg_taken_{index}')
                map_data['blue_mid_dmg_taken'] = st.text_input(
                    'Blue Mid DMG Taken', key=f'blue_mid_dmg_taken_{index}')
                map_data['blue_dragon_dmg_taken'] = st.text_input(
                    'Blue Dragon DMG Taken', key=f'blue_dragon_dmg_taken_{index}')
                map_data['blue_sup_dmg_taken'] = st.text_input(
                    'Blue Sup DMG Taken', key=f'blue_sup_dmg_taken_{index}')
            with blue_gold:
                map_data['blue_baron_total_gold'] = st.text_input(
                    'Blue Baron Gold', key=f'blue_baron_total_gold_{index}')
                map_data['blue_jungle_total_gold'] = st.text_input(
                    'Blue Jungle Gold', key=f'blue_jungle_total_gold_{index}')
                map_data['blue_mid_total_gold'] = st.text_input(
                    'Blue Mid Gold', key=f'blue_mid_total_gold_{index}')
                map_data['blue_dragon_total_gold'] = st.text_input(
                    'Blue Dragon Gold', key=f'blue_dragon_total_gold_{index}')
                map_data['blue_sup_total_gold'] = st.text_input(
                    'Blue Sup Gold', key=f'blue_sup_total_gold_{index}')
            with red_dmg_dealt:
                map_data['red_baron_dmg_dealt'] = st.text_input(
                    'Red Baron DMG Dealt', key=f'red_baron_dmg_dealt_{index}')
                map_data['red_jungle_dmg_dealt'] = st.text_input(
                    'Red Jungle DMG Dealt', key=f'red_jungle_dmg_dealt_{index}')
                map_data['red_mid_dmg_dealt'] = st.text_input(
                    'Red Mid DMG Dealt', key=f'red_mid_dmg_dealt_{index}')
                map_data['red_dragon_dmg_dealt'] = st.text_input(
                    'Red Dragon DMG Dealt', key=f'red_dragon_dmg_dealt_{index}')
                map_data['red_sup_dmg_dealt'] = st.text_input(
                    'Red Sup DMG Dealt', key=f'red_sup_dmg_dealt_{index}')
            with red_dmg_taken:
                map_data['red_baron_dmg_taken'] = st.text_input(
                    'Red Baron DMG Taken', key=f'red_baron_dmg_taken_{index}')
                map_data['red_jungle_dmg_taken'] = st.text_input(
                    'Red Jungle DMG Taken', key=f'red_jungle_dmg_taken_{index}')
                map_data['red_mid_dmg_taken'] = st.text_input(
                    'Red Mid DMG Taken', key=f'red_mid_dmg_taken_{index}')
                map_data['red_dragon_dmg_taken'] = st.text_input(
                    'Red Dragon DMG Taken', key=f'red_dragon_dmg_taken_{index}')
                map_data['red_sup_dmg_taken'] = st.text_input(
                    'Red Sup DMG Taken', key=f'red_sup_dmg_taken_{index}')
            with red_gold:
                map_data['red_baron_total_gold'] = st.text_input(
                    'Red Baron Gold', key=f'red_baron_total_gold_{index}')
                map_data['red_jungle_total_gold'] = st.text_input(
                    'Red Jungle Gold', key=f'red_jungle_total_gold_{index}')
                map_data['red_mid_total_gold'] = st.text_input(
                    'Red Mid Gold', key=f'red_mid_total_gold_{index}')
                map_data['red_dragon_total_gold'] = st.text_input(
                    'Red Dragon Gold', key=f'red_dragon_total_gold_{index}')
                map_data['red_sup_total_gold'] = st.text_input(
                    'Red Sup Gold', key=f'red_sup_total_gold_{index}')

    maps.append(map_data)

st.button("Save", on_click=format_official)
