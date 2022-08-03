from datetime import timedelta
from shillelagh.backends.apsw.db import connect
from queries import (
    patches_query, phases_query, teams_query,
    ROLE_QUERY, TOURNAMENT_QUERY,
    prio_query, blind_response_query,
    match_stats_df, picks_bans_df, total_games_query
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


@st.cache(ttl=600)
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


general_tab, picks_tab, bans_tab, presence_tab = st.tabs(["Geral", "Picks", "Bans", "Prsença"])

tournaments = st.sidebar.multiselect(
    'Campeonatos', sum(run_query(TOURNAMENT_QUERY), ()), ['VG Open 2022'])
patches = st.sidebar.multiselect('Patch', sum(run_query(patches_query(tournaments)), ()))
phases = st.sidebar.multiselect('Fase', sum(run_query(phases_query(tournaments)), ()))
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
        st.dataframe(pr_df)
        st.title('Blind rate')
        st.dataframe(blind_df)
        st.title('Response rate')
        st.dataframe(response_df)
    with col2:
        st.title('Win rate')
        st.dataframe(wr_df)
        st.title('Win rate')
        st.dataframe(blind_wr_df)
        st.title('Win rate')
        st.dataframe(response_wr_df)
