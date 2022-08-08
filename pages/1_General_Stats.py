from datetime import timedelta
from shillelagh.backends.apsw.db import connect
from queries import (
    patches_query, phases_query, teams_query,
    ROLE_QUERY, TOURNAMENT_QUERY, general_stats_query,
    picks_bans_df, match_stats_df
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


team_tab, player_tab, champion_tab = st.tabs(["Team", "Player", "Champion"])

tournaments = st.sidebar.multiselect(
    'Campeonatos', sum(run_query(TOURNAMENT_QUERY), ()))
patches = st.sidebar.multiselect('Patch', sum(run_query(patches_query(tournaments)), ()))
phases = st.sidebar.multiselect('Fase', sum(run_query(phases_query(tournaments)), ()))
teams = st.sidebar.multiselect('Time', sum(run_query(teams_query(tournaments)), ()))
roles = st.sidebar.multiselect('Role', sum(run_query(ROLE_QUERY), ()))

with team_tab:

    team_df = pd.DataFrame(
        run_query(general_stats_query(patches=patches, phases=phases, tournaments=tournaments,
                                      columns='team_name, team_tag', is_team=True, df='match_stats_df')),
        columns=[
            'team', 'tag', 'QTY Games', '%WR', 'QTY Blue', '%WR Blue', 'QTY Red', '%WR Red', 'AGT', 'AGT Win',
            'AGT Loss'
        ])
    team_df['%WR'] = (team_df['%WR'] / team_df['QTY Games']) * 100
    team_df['%WR Blue'] = (team_df['%WR Blue'] / team_df['QTY Blue']) * 100
    team_df['%WR Red'] = (team_df['%WR Red'] / team_df['QTY Red']) * 100
    # agt = team_df['AGT'].mean()
    # if agt != np.nan:
    #     agt = str(timedelta(seconds=agt)).split(':')
    #     agt = f'{agt[1]}:{agt[2][:2]}'
    for colum in TIME_COLUMNS:
        team_df[colum] = pd.to_datetime(team_df[colum], unit='s').dt.strftime("%M:%S")
        team_df[colum] = team_df[colum].replace(np.nan, '-')
    team_df.style.format(precision=2)
    col1, col2, col3, col4 = st.columns(4)
    team_column1 = col1.selectbox('Column 1', team_df.keys(), 0, key='team_select_col_1')
    team_sort1 = col2.selectbox('Sort column 1', ['ASC', 'DESC'], key='team_select_sort_1')
    team_column2 = col3.selectbox('Column 2', [c for c in team_df.keys() if c != team_column1], 0, key='team_select_col_2')
    team_sort2 = col4.selectbox('Sort column 2', ['ASC', 'DESC'], key='team_select_sort_2')
    team_df.sort_values([team_column1, team_column2], ascending=[team_sort1 == 'ASC', team_sort2 == 'ASC'], inplace=True)
    st.table(team_df.style.format(precision=2).format(subset=INT_COLUMNS, formatter='{:.0f}'))

with player_tab:
    player_df = pd.DataFrame(
        run_query(general_stats_query(patches, phases, teams, roles, tournaments, columns='role, player')), columns=[
            'Role', 'Player', 'AVG Kills', 'AVG Deaths', 'AVG Assists', 'AVG KDA',
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
    player_df.style.format(precision=2)
    col1, col2, col3, col4 = st.columns(4)
    column1 = col1.selectbox('Column 1', player_df.keys(), key='player_select_col_1')
    sort1 = col2.selectbox('Sort column 1', ['ASC', 'DESC'], key='player_select_sort_1')
    column2 = col3.selectbox('Column 2', [c for c in player_df.keys() if c != column1], 0, key='player_select_col_2')
    sort2 = col4.selectbox('Sort column 2', ['ASC', 'DESC'], key='player_select_sort_2')
    player_df.sort_values([column1, column2], ascending=[sort1 == 'ASC', sort2 == 'ASC'], inplace=True)
    st.table(
        player_df.style.format(precision=2).format(subset=[*INT_COLUMNS, *INDIVIDUAL_COLUMNS],
                                                   formatter='{:.0f}'))

with champion_tab:
    champion_df = pd.DataFrame(run_query(general_stats_query(patches, phases, teams, roles, tournaments)), columns=[
        'Pick', 'AVG Kills', 'AVG Deaths', 'AVG Assists', 'AVG KDA',
        'AVG DDPM', 'AVG DTPM', 'AVG GPM', 'AVG DDPG', 'AVG DTPG',
        'QTY Games', '%WR', 'QTY Blue', '%WR Blue', 'QTY Red', '%WR Red',
        'AGT', 'AGT Win', 'AGT Loss'
    ])
    for colum in TIME_COLUMNS:
        champion_df[colum] = pd.to_datetime(champion_df[colum], unit='s').dt.strftime("%M:%S")
        champion_df[colum] = champion_df[colum].replace(np.nan, '-')
    champion_df['AVG KDA'] = (champion_df['AVG Kills'] + champion_df['AVG Assists']) / champion_df['AVG Deaths']
    champion_df['AVG DDPG'] = champion_df['AVG DDPM'] / champion_df['AVG GPM']
    champion_df['AVG DTPG'] = champion_df['AVG DTPM'] / champion_df['AVG GPM']
    champion_df.style.format(precision=2)
    col1, col2, col3, col4 = st.columns(4)
    column1 = col1.selectbox('Column 1', champion_df.keys(), key='champion_select_col_1')
    sort1 = col2.selectbox('Sort column 1', ['ASC', 'DESC'], key='champion_select_sort_1')
    column2 = col3.selectbox('Column 2', [c for c in champion_df.keys() if c != column1], 0, key='champion_select_col_2')
    sort2 = col4.selectbox('Sort column 2', ['ASC', 'DESC'], key='champion_select_sort_2')
    champion_df.sort_values([column1, column2], ascending=[sort1 == 'ASC', sort2 == 'ASC'], inplace=True)
    st.table(champion_df.style.format(precision=2).format(subset=[*INT_COLUMNS, *INDIVIDUAL_COLUMNS], formatter='{:.0f}'))