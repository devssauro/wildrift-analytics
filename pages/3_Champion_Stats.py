from datetime import timedelta
from shillelagh.backends.apsw.db import connect
from queries import (
    patches_query, phases_query, teams_query,
    role_query, TOURNAMENT_QUERY,
    champion_df, general_stats_query,
    champion_maps_query, champion_matchup_query,
    picks_bans_df, match_stats_df
)
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Champion",
    page_icon="👋",
    layout="wide"
)

connection = connect(':memory:')
cursor = connection.cursor()

st.title("Champion stats")
INDIVIDUAL_COLUMNS = ['AVG DDPM', 'AVG DTPM', 'AVG GPM']
INT_COLUMNS = ['QTY Games', 'QTY Blue', 'QTY Red']
TIME_COLUMNS = ['AGT', 'AGT Win', 'AGT Loss']


@st.cache(ttl=600)
def run_query(query):
    rows = cursor.execute(query)
    return rows.fetchall()


matchup_tab, players_tab = st.tabs(["Matchups", "Jogadores"])

tournaments = st.sidebar.multiselect(
    'Campeonatos', sum(run_query(TOURNAMENT_QUERY), ()), ['VG Open 2022'])
patches = st.sidebar.multiselect('Patch', sum(run_query(patches_query(tournaments)), ()))
phases = st.sidebar.multiselect('Fase', sum(run_query(phases_query(tournaments)), ()))
teams = st.sidebar.multiselect('Time', sum(run_query(teams_query(tournaments)), ()))
champion = st.sidebar.selectbox('Champion', champion_df['name'])
roles = st.sidebar.multiselect('Role', sum(run_query(role_query(champion)), ()))

with matchup_tab:
    all_roles = ['baron', 'jungle', 'mid', 'dragon', 'sup']
    selected_roles = roles if len(roles) > 0 else all_roles
    maps = sum(run_query(champion_maps_query(
        patches, phases, teams, selected_roles, tournaments, champion)), ())
    q_with = pd.DataFrame()
    q_against = pd.DataFrame()
    col1, col2, col3, col4 = st.columns(4)
    sort_columns = ['Pick', 'Qty Pick', 'Qty Win', '%WR']
    pick_column1 = col1.selectbox('Column 1', sort_columns, key='pick_select_col_1')
    pick_sort1 = col2.selectbox('Sort column 1', ['ASC', 'DESC'], key='pick_select_sort_1')
    pick_column2 = col3.selectbox('Column 2', [c for c in sort_columns if c != pick_column1], key='pick_select_col_2')
    pick_sort2 = col4.selectbox('Sort column 2', ['ASC', 'DESC'], key='pick_select_sort_2')
    for _role in all_roles:
        temp_against = pd.DataFrame(run_query(champion_matchup_query(
            patches, phases, teams, roles, tournaments, champion, role=_role, maps=maps, selected_roles=selected_roles)),
            columns=['Pick', 'Role', 'Qty Pick', 'Qty Win']
        )
        temp_against.sort_values([pick_column1, pick_column2],
                                 ascending=[pick_sort1 == 'ASC', pick_sort2 == 'ASC'], inplace=True)
        q_against = pd.concat([q_against, temp_against])
        temp_with = pd.DataFrame(run_query(champion_matchup_query(
            patches, phases, teams, roles, tournaments, champion, role=_role, maps=maps, against=False, selected_roles=selected_roles)),
            columns=['Pick', 'Role', 'Qty Pick', 'Qty Win']
        )
        temp_with.sort_values([pick_column1, pick_column2],
                              ascending=[pick_sort1 == 'ASC', pick_sort2 == 'ASC'], inplace=True)
        q_with = pd.concat([q_with, temp_with])
    q_with['%WR'] = (q_with['Qty Win'] / q_with['Qty Pick']) * 100
    q_against['%WR'] = (q_against['Qty Win'] / q_against['Qty Pick']) * 100
    _col1, _col2 = st.columns(2)
    with _col1:
        st.title('Played With')
        st.table(q_with.style.format(precision=2))
    with _col2:
        st.title('Played Against')
        st.table(q_against.style.format(precision=2))

with players_tab:
    player_df = pd.DataFrame(
        run_query(general_stats_query(patches, phases, teams, roles, tournaments, columns='player', champion=champion)),
        columns=[
            'Player', 'AVG Kills', 'AVG Deaths', 'AVG Assists', 'AVG KDA',
            'AVG DDPM', 'AVG DTPM', 'AVG GPM', 'AVG DDPG', 'AVG DTPG',
            'QTY Games', '%WR', 'QTY Blue', '%WR Blue', 'QTY Red', '%WR Red',
            'AGT', 'AGT Win', 'AGT Loss'
        ]
    )
    for colum in TIME_COLUMNS:
        player_df[colum] = pd.to_datetime(player_df[colum], unit='s').dt.strftime("%M:%S")
        player_df[colum] = player_df[colum].replace(np.nan, '-')
    player_df['AVG KDA'] = (player_df['AVG Kills'] + player_df['AVG Assists']) / player_df['AVG Deaths']
    player_df['AVG DDPG'] = player_df['AVG DDPM'] / player_df['AVG GPM']
    player_df['AVG DTPG'] = player_df['AVG DTPM'] / player_df['AVG GPM']
    player_df['%WR'] = (player_df['%WR'] / player_df['QTY Games']) * 100
    player_df['%WR Blue'] = (player_df['%WR Blue'] / player_df['QTY Blue']) * 100
    player_df['%WR Red'] = (player_df['%WR Red'] / player_df['QTY Red']) * 100
    player_df.style.format(precision=2)
    col1, col2, col3, col4 = st.columns(4)
    player_column1 = col1.selectbox('Column 1', player_df.keys(), key='player_select_col_1')
    player_sort1 = col2.selectbox('Sort column 1', ['ASC', 'DESC'], key='player_select_sort_1')
    player_column2 = col3.selectbox('Column 2', [c for c in player_df.keys() if c != player_column1], key='player_select_col_2')
    player_sort2 = col4.selectbox('Sort column 2', ['ASC', 'DESC'], key='player_select_sort_2')
    player_df.sort_values([player_column1, player_column2],
                          ascending=[player_sort1 == 'ASC', player_sort2 == 'ASC'], inplace=True)
    st.table(player_df.style.format(precision=2).format(
        subset=[*INT_COLUMNS, *INDIVIDUAL_COLUMNS], formatter='{:.0f}'))
