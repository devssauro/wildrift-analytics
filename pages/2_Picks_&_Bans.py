from datetime import timedelta
from shillelagh.backends.apsw.db import connect
from queries import (
    patches_query, phases_query, teams_query,
    ROLE_QUERY, TOURNAMENT_QUERY, CHAMPION_ROLE_QUERY,
    prio_query, blind_response_query,
    match_stats_df, picks_bans_df, total_games_query,
    picks_bans_query, presence_query
)
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="General Stats - Champion",
    page_icon="👋",
    layout="wide"
)

connection = connect(':memory:')
cursor = connection.cursor()

st.title("General stats")
INDIVIDUAL_COLUMNS = ['AVG DDPM', 'AVG DTPM', 'AVG GPM']
INT_COLUMNS = ['QTY Games', 'QTY Blue', 'QTY Red']
TIME_COLUMNS = ['AGT', 'AGT Win', 'AGT Loss']


def run_query(query):
    rows = cursor.execute(query)
    return rows.fetchall()


def prio_percent(picks: int, games: int, side: str, rotation: str):
    if games == 0:
        return '0.0%'
    if rotation in ('B1', 'R3', 'R4', 'R5'):
        return f'{round((picks / games) * 100, 2)}%'
    else:
        return f'{round((picks / games) * 100, 2)}%'


def prio_percent_wr(picks: int, games: int, side: str, rotation: str, role: str):
    if picks == 0:
        return '-'
    if rotation in ('B1', 'R3', 'R4', 'R5'):
        return f'{round((games / picks) * 100, 2)}%'
    else:
        return f'{round((games / picks) * 100, 2)}%'


general_tab, picks_bans_tab, presence_tab = st.tabs(["Geral", "Picks & Bans", "Presença"])

tournaments = st.sidebar.multiselect(
    'Campeonatos', sum(run_query(TOURNAMENT_QUERY), ()))
patches = st.sidebar.multiselect('Patch', sum(run_query(patches_query(tournaments)), ()))
phases = st.sidebar.multiselect('Fase', [p for p in sum(run_query(phases_query(tournaments)), ()) if p is not None])
teams = st.sidebar.multiselect('Time', sum(run_query(teams_query(tournaments)), ()))
roles = st.sidebar.multiselect('Role', sum(run_query(ROLE_QUERY), ()))

with general_tab:
    col1, col2 = st.columns(2)

    # Pick rate and Win Rate
    final_list = []
    wr_list = []
    prio_df = pd.DataFrame(
        run_query(prio_query(patches=patches, phases=phases, tournaments=tournaments)),
        columns=['side', 'pick_rotation', 'role', 'total', 'total_win']
    )

    total_games = run_query(total_games_query(patches=patches, phases=phases, tournaments=tournaments))[0][0]
    total_games = {
        'blue': total_games,
        'red': total_games,
    }
    prio_role = {'blue': {'B1': {}, 'B2/B3': {}, 'B4/B5': {}}, 'red': {'R1/R2': {}, 'R3': {}, 'R4': {}, 'R5': {}}}
    wr_role = {'blue': {'B1': {}, 'B2/B3': {}, 'B4/B5': {}}, 'red': {'R1/R2': {}, 'R3': {}, 'R4': {}, 'R5': {}}}
    for row in prio_df.T.to_dict().values():
        prio_role[row['side']][row['pick_rotation']][row['role']] = row['total']
        wr_role[row['side']][row['pick_rotation']][row['role']] = row['total_win']

    for side in prio_role.keys():
        for rotation in prio_role[side].keys():
            final_list.append({
                'side': side,
                'rotation': rotation,
                'baron': prio_percent(
                    prio_role[side][rotation].get('baron', 0), total_games[side], side, rotation),
                'jungle': prio_percent(
                    prio_role[side][rotation].get('jungle', 0), total_games[side], side, rotation),
                'mid': prio_percent(
                    prio_role[side][rotation].get('mid', 0), total_games[side], side, rotation),
                'dragon': prio_percent(
                    prio_role[side][rotation].get('dragon', 0), total_games[side], side, rotation),
                'sup': prio_percent(
                    prio_role[side][rotation].get('sup', 0), total_games[side], side, rotation)
            })
            wr_list.append({
                'side': side,
                'rotation': rotation,
                'baron': prio_percent_wr(
                    prio_role[side][rotation].get('baron', 0), wr_role[side][rotation].get('baron', 0), side, rotation,
                    'baron'),
                'jungle': prio_percent_wr(
                    prio_role[side][rotation].get('jungle', 0), wr_role[side][rotation].get('jungle', 0), side,
                    rotation, 'jungle'),
                'mid': prio_percent_wr(
                    prio_role[side][rotation].get('mid', 0), wr_role[side][rotation].get('mid', 0), side, rotation,
                    'mid'),
                'dragon': prio_percent_wr(
                    prio_role[side][rotation].get('dragon', 0), wr_role[side][rotation].get('dragon', 0), side,
                    rotation, 'dragon'),
                'sup': prio_percent_wr(
                    prio_role[side][rotation].get('sup', 0), wr_role[side][rotation].get('sup', 0), side, rotation,
                    'sup')
            })
    pr_df = pd.DataFrame(final_list)
    wr_df = pd.DataFrame(wr_list)
    pr_df.drop('side', axis=1, inplace=True)
    wr_df.drop('side', axis=1, inplace=True)

    pr_df.style.format(precision=2)
    wr_df.style.format(precision=2)

    # Blind and Response Rate
    blind_role = {
        'blue': {
            'total': {
                'total_blind': {'baron': 0, 'jungle': 0, 'mid': 0, 'dragon': 0, 'sup': 0},
                'win_blind': {'baron': 0, 'jungle': 0, 'mid': 0, 'dragon': 0, 'sup': 0},
                'total_response': {'baron': 0, 'jungle': 0, 'mid': 0, 'dragon': 0, 'sup': 0},
                'win_response': {'baron': 0, 'jungle': 0, 'mid': 0, 'dragon': 0, 'sup': 0}
            },
            'B1': {'baron': {}, 'jungle': {}, 'mid': {}, 'dragon': {}, 'sup': {}},
            'B2/B3': {'baron': {}, 'jungle': {}, 'mid': {}, 'dragon': {}, 'sup': {}},
            'B4/B5': {'baron': {}, 'jungle': {}, 'mid': {}, 'dragon': {}, 'sup': {}}
        },
        'red': {
            'total': {
                'total_blind': {'baron': 0, 'jungle': 0, 'mid': 0, 'dragon': 0, 'sup': 0},
                'win_blind': {'baron': 0, 'jungle': 0, 'mid': 0, 'dragon': 0, 'sup': 0},
                'total_response': {'baron': 0, 'jungle': 0, 'mid': 0, 'dragon': 0, 'sup': 0},
                'win_response': {'baron': 0, 'jungle': 0, 'mid': 0, 'dragon': 0, 'sup': 0}
            },
            'R1/R2': {'baron': {}, 'jungle': {}, 'mid': {}, 'dragon': {}, 'sup': {}},
            'R3': {'baron': {}, 'jungle': {}, 'mid': {}, 'dragon': {}, 'sup': {}},
            'R4': {'baron': {}, 'jungle': {}, 'mid': {}, 'dragon': {}, 'sup': {}},
            'R5': {'baron': {}, 'jungle': {}, 'mid': {}, 'dragon': {}, 'sup': {}}
        }
    }
    br_df = pd.DataFrame(
        run_query(blind_response_query(patches=patches, phases=phases, tournaments=tournaments)),
        columns=['side', 'pick_rotation', 'role', 'total_blind', 'win_blind', 'total_response', 'win_response']
    )

    for row in br_df.T.to_dict().values():
        blind_role[row['side']][row['pick_rotation']][row['role']]['total_blind'] = row['total_blind']
        blind_role[row['side']][row['pick_rotation']][row['role']]['win_blind'] = row['win_blind']
        blind_role[row['side']][row['pick_rotation']][row['role']]['total_response'] = row['total_response']
        blind_role[row['side']][row['pick_rotation']][row['role']]['win_response'] = row['win_response']
    blind_list = []
    blind_wr_list = []
    response_list = []
    response_wr_list = []
    for side in blind_role.keys():
        for rotation in [r for r in blind_role[side].keys() if r != 'total']:
            blind_list.append({
                'side': side,
                'rotation': rotation,
                'baron': prio_percent(
                    blind_role[side][rotation]['baron'].get('total_blind', 0), total_games[side], side, rotation),
                'jungle': prio_percent(
                    blind_role[side][rotation]['jungle'].get('total_blind', 0), total_games[side], side, rotation),
                'mid': prio_percent(
                    blind_role[side][rotation]['mid'].get('total_blind', 0), total_games[side], side, rotation),
                'dragon': prio_percent(
                    blind_role[side][rotation]['dragon'].get('total_blind', 0), total_games[side], side, rotation),
                'sup': prio_percent(
                    blind_role[side][rotation]['sup'].get('total_blind', 0), total_games[side], side, rotation)
            })
            blind_wr_list.append({
                'side': side,
                'rotation': rotation,
                'baron': prio_percent_wr(
                    blind_role[side][rotation]['baron'].get('total_blind', 0),
                    blind_role[side][rotation]['baron'].get('win_blind', 0), side, rotation, 'baron'),
                'jungle': prio_percent_wr(
                    blind_role[side][rotation]['jungle'].get('total_blind', 0),
                    blind_role[side][rotation]['jungle'].get('win_blind', 0), side, rotation, 'jungle'),
                'mid': prio_percent_wr(
                    blind_role[side][rotation]['mid'].get('total_blind', 0),
                    blind_role[side][rotation]['mid'].get('win_blind', 0), side, rotation, 'mid'),
                'dragon': prio_percent_wr(
                    blind_role[side][rotation]['dragon'].get('total_blind', 0),
                    blind_role[side][rotation]['dragon'].get('win_blind', 0), side, rotation, 'dragon'),
                'sup': prio_percent_wr(
                    blind_role[side][rotation]['sup'].get('total_blind', 0),
                    blind_role[side][rotation]['sup'].get('win_blind', 0), side, rotation, 'sup')
            })
            response_list.append({
                'side': side,
                'rotation': rotation,
                'baron': prio_percent(
                    blind_role[side][rotation]['baron'].get('total_response', 0), total_games[side], side, rotation),
                'jungle': prio_percent(
                    blind_role[side][rotation]['jungle'].get('total_response', 0), total_games[side], side, rotation),
                'mid': prio_percent(
                    blind_role[side][rotation]['mid'].get('total_response', 0), total_games[side], side, rotation),
                'dragon': prio_percent(
                    blind_role[side][rotation]['dragon'].get('total_response', 0), total_games[side], side, rotation),
                'sup': prio_percent(
                    blind_role[side][rotation]['sup'].get('total_response', 0), total_games[side], side, rotation)
            })
            response_wr_list.append({
                'side': side,
                'rotation': rotation,
                'baron': prio_percent_wr(
                    blind_role[side][rotation]['baron'].get('total_response', 0),
                    blind_role[side][rotation]['baron'].get('win_response', 0), side, rotation, 'baron'),
                'jungle': prio_percent_wr(
                    blind_role[side][rotation]['jungle'].get('total_response', 0),
                    blind_role[side][rotation]['jungle'].get('win_response', 0), side, rotation, 'jungle'),
                'mid': prio_percent_wr(
                    blind_role[side][rotation]['mid'].get('total_response', 0),
                    blind_role[side][rotation]['mid'].get('win_response', 0), side, rotation, 'mid'),
                'dragon': prio_percent_wr(
                    blind_role[side][rotation]['dragon'].get('total_response', 0),
                    blind_role[side][rotation]['dragon'].get('win_response', 0), side, rotation, 'dragon'),
                'sup': prio_percent_wr(
                    blind_role[side][rotation]['sup'].get('total_response', 0),
                    blind_role[side][rotation]['sup'].get('win_response', 0), side, rotation, 'sup')
            })
    blind_df = pd.DataFrame(blind_list)
    blind_wr_df = pd.DataFrame(blind_wr_list)
    blind_df.drop('side', axis=1, inplace=True)
    blind_wr_df.drop('side', axis=1, inplace=True)

    response_df = pd.DataFrame(response_list)
    response_wr_df = pd.DataFrame(response_wr_list)
    response_df.drop('side', axis=1, inplace=True)
    response_wr_df.drop('side', axis=1, inplace=True)

    blind_df.style.format(precision=2)
    blind_wr_df.style.format(precision=2)
    response_df.style.format(precision=2)
    response_wr_df.style.format(precision=2)

    with col1:
        st.title('Pick rate')
        st.table(pr_df)
        st.title('Blind rate')
        st.table(blind_df)
        st.title('Response rate')
        st.table(response_df)
    with col2:
        st.title('Win rate')
        st.table(wr_df)
        st.title('Win rate')
        st.table(blind_wr_df)
        st.title('Win rate')
        st.table(response_wr_df)

with picks_bans_tab:
    col1, col2, col3, col4 = st.columns(4)
    sorteable_columns = ['Pick', 'Qty Pick', 'Qty win', '%WR']
    pb_column1 = col1.selectbox('Column 1', sorteable_columns, key='pb_select_col_1')
    pb_sort1 = col2.selectbox('Sort column 1', ['ASC', 'DESC'], key='pb_select_sort_1')
    pb_column2 = col3.selectbox('Column 2', [c for c in sorteable_columns if c != pb_column1], key='pb_select_col_2')
    pb_sort2 = col4.selectbox('Sort column 2', ['ASC', 'DESC'], key='pb_select_sort_2')
    # player_df.sort_values([player_column1, player_column2],
    #                       ascending=[player_sort1 == 'ASC', player_sort2 == 'ASC'], inplace=True)

    with col1:
        st.title('Pick blue')
        pick_blue_df = pd.DataFrame(
            run_query(picks_bans_query(
                patches=patches, phases=phases, tournaments=tournaments)),
            columns=['Pick', 'Rotation', 'Qty Pick', 'Qty win']
        )
        pick_blue_df['%WR'] = (pick_blue_df['Qty win'] / pick_blue_df['Qty Pick']) * 100
        pick_blue_df.sort_values(['Rotation', pb_column1, pb_column2],
                                 ascending=[True, pb_sort1 == 'ASC', pb_sort2 == 'ASC'], inplace=True)
        st.table(pick_blue_df.style.format(precision=2))
    with col2:
        st.title('Pick red')
        pick_red_df = pd.DataFrame(
            run_query(picks_bans_query(
                patches=patches, phases=phases, tournaments=tournaments, side='red')),
            columns=['Pick', 'Rotation', 'Qty Pick', 'Qty win']
        )
        pick_red_df['%WR'] = (pick_red_df['Qty win'] / pick_red_df['Qty Pick']) * 100
        pick_red_df.sort_values(['Rotation', pb_column1, pb_column2],
                                 ascending=[True, pb_sort1 == 'ASC', pb_sort2 == 'ASC'], inplace=True)
        st.table(pick_red_df.style.format(precision=2))
    with col3:
        st.title('Ban blue')
        ban_blue_df = pd.DataFrame(
            run_query(picks_bans_query(
                patches=patches, phases=phases, tournaments=tournaments, pick_ban='ban')),
            columns=['Pick', 'Rotation', 'Qty Pick', 'Qty win']
        )
        ban_blue_df['%WR'] = (ban_blue_df['Qty win'] / ban_blue_df['Qty Pick']) * 100
        ban_blue_df.sort_values(['Rotation', pb_column1, pb_column2],
                                 ascending=[True, pb_sort1 == 'ASC', pb_sort2 == 'ASC'], inplace=True)
        st.table(ban_blue_df.style.format(precision=2))
    with col4:
        st.title('Ban red')
        ban_red_df = pd.DataFrame(
            run_query(picks_bans_query(
                patches=patches, phases=phases, tournaments=tournaments, pick_ban='ban', side='red')),
            columns=['Pick', 'Rotation', 'Qty Pick', 'Qty win']
        )
        ban_red_df['%WR'] = (ban_red_df['Qty win'] / ban_red_df['Qty Pick']) * 100
        ban_red_df.sort_values(['Rotation', pb_column1, pb_column2],
                               ascending=[True, pb_sort1 == 'ASC', pb_sort2 == 'ASC'], inplace=True)
        st.table(ban_red_df.style.format(precision=2))

with presence_tab:
    champions = pd.DataFrame(run_query(CHAMPION_ROLE_QUERY), columns=['pick', 'role']).T.to_dict().values()
    pick_presence = pd.DataFrame(
        run_query(presence_query(
            patches=patches, phases=phases, tournaments=tournaments)),
        columns=['pick', 'role', 'qty_picks', 'qty_win']
    )
    pick_dict = pick_presence.T.to_dict().values()

    ban_presence = pd.DataFrame(
        run_query(presence_query(
            patches=patches, phases=phases, tournaments=tournaments, pick_ban='ban')),
        columns=['ban', 'role', 'qty_bans', 'qty_win']
    )
    ban_dict = ban_presence.T.to_dict().values()
    # st.write(ban_dict)
    total_games = run_query(total_games_query(patches=patches, phases=phases, tournaments=tournaments))[0][0]
    roles = ['baron', 'jungle', 'mid', 'dragon', 'sup']
    data = {r: [] for r in roles}
    for c in champions:
        pick_presence = [row for row in pick_dict if row['role'] == c['role'] and row['pick'] == c['pick']]
        win_presence = [row for row in pick_dict if row['role'] == c['role'] and row['pick'] == c['pick']]
        ban_presence = [row for row in ban_dict if row['ban'] == c['pick']]
        if len(pick_presence) > 0 or len(ban_presence):
            qty_picks = 0 if len(pick_presence) == 0 else pick_presence[0]['qty_picks']
            qty_win = 0 if len(win_presence) == 0 else win_presence[0]['qty_win']
            qty_bans = 0 if len(ban_presence) == 0 else ban_presence[0]['qty_bans']
            qty_presence = qty_picks + qty_bans
            _temp = {
                'champion': c['pick'],
                'picks': qty_picks,
                'bans': qty_bans,
                'win': qty_win,
                'presence': qty_presence,
                '%win': np.nan if qty_picks == 0 else round((qty_win / qty_picks) * 100, 2),
                '%pres': np.nan if qty_presence == 0 else round((qty_presence / total_games) * 100, 2),
            }
            if c['role'] is not None:
                data[c['role']].append({**_temp, 'presence': _temp['picks'] + _temp['bans']})
    baron, jungle, mid, dragon, sup = st.columns(len(roles))
    with baron:
        st.title('Baron')
        baron_df = pd.DataFrame(data['baron'])
        st.dataframe(baron_df.style.format(precision=2))
    with jungle:
        st.title('Jungle')
        jungle_df = pd.DataFrame(data['jungle'])
        st.dataframe(jungle_df.style.format(precision=2))
    with mid:
        st.title('Mid')
        mid_df = pd.DataFrame(data['mid'])
        st.dataframe(mid_df.style.format(precision=2))
    with dragon:
        st.title('Dragon')
        dragon_df = pd.DataFrame(data['dragon'])
        st.dataframe(dragon_df.style.format(precision=2))
    with sup:
        st.title('Sup')
        sup_df = pd.DataFrame(data['sup'])
        st.dataframe(sup_df.style.format(precision=2))
