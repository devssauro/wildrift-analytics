from datetime import timedelta
from shillelagh.backends.apsw.db import connect
from queries import patches_query, phases_query, ROLE_QUERY, teams_query, TOURNAMENT_QUERY, general_stats_query
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
individual_df = pd.read_csv(
    'https://wrflask.dinossauro.dev/v1/download/picks_bans'
    '?winner_loser=binary&blind_response=binary&pick_rotation=explicit_eng'
)
teams_df = pd.read_csv(
    'https://wrflask.dinossauro.dev/v1/download/match_stats'
    '?winner_loser=binary&blind_response=binary&pick_rotation=explicit_eng'
)
champion_df = pd.read_csv('champion.csv')

st.title("General stats")
INDIVIDUAL_COLUMNS = ['AVG DDPM', 'AVG DTPM', 'AVG GPM']
INT_COLUMNS = ['QTY Games', 'QTY Blue', 'QTY Red']
TIME_COLUMNS = ['AGT', 'AGT Win', 'AGT Loss']


@st.cache(ttl=600)
def run_query(query):
    rows = cursor.execute(query)
    return rows.fetchall()


team_tab, player_tab, champion_tab = st.tabs(["Team", "Player", "Champion"])

tournaments = st.sidebar.multiselect('Campeonatos', sum(run_query(TOURNAMENT_QUERY), ()))
patches = st.sidebar.multiselect('Patch', sum(run_query(patches_query(tournaments)), ()))
phases = st.sidebar.multiselect('Fase', sum(run_query(phases_query(tournaments)), ()))
teams = st.sidebar.multiselect('Time', sum(run_query(teams_query(tournaments)), ()))
roles = st.sidebar.multiselect('Role', sum(run_query(ROLE_QUERY), ()))

with team_tab:
    team_df = pd.DataFrame(
        run_query(general_stats_query(patches=patches, phases=phases, tournaments=tournaments,
                                      columns='team_name, team_tag', is_team=True, df='teams_df')),
        columns=[
            'team', 'tag', 'QTY Games', '%WR', 'QTY Blue', '%WR Blue', 'QTY Red', '%WR Red', 'AGT', 'AGT Win',
            'AGT Loss'
        ])
    team_df['%WR'] = (team_df['%WR'] / team_df['QTY Games']) * 100
    team_df['%WR Blue'] = (team_df['%WR Blue'] / team_df['QTY Blue']) * 100
    team_df['%WR Red'] = (team_df['%WR Red'] / team_df['QTY Red']) * 100
    agt = team_df['AGT'].mean()
    agt = str(timedelta(seconds=agt)).split(':')
    agt = f'{agt[1]}:{agt[2][:2]}'
    for colum in TIME_COLUMNS:
        team_df[colum] = pd.to_datetime(team_df[colum], unit='s').dt.strftime("%M:%S")
        team_df[colum] = team_df[colum].replace(np.nan, '-')
    team_df.style.format(precision=2)
    st.dataframe(team_df.style.format(precision=2).format(subset=INT_COLUMNS, formatter='{:.0f}'))

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
    st.dataframe(
        player_df.style.format(precision=2).format(subset=[*INT_COLUMNS, *INDIVIDUAL_COLUMNS],
                                                   formatter='{:.0f}'), height=550)

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
    st.dataframe(champion_df.style.format(precision=2).format(subset=[*INT_COLUMNS, *INDIVIDUAL_COLUMNS],
                                                              formatter='{:.0f}'), height=550)
