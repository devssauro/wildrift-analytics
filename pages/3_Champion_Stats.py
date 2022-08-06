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
    col1, col2 = st.columns(2)
    all_roles = ['baron', 'jungle', 'mid', 'dragon', 'sup']
    selected_roles = roles if len(roles) > 0 else all_roles
    maps = sum(run_query(champion_maps_query(
        patches, phases, teams, selected_roles, tournaments, champion)), ())
    q_with = pd.DataFrame()
    q_against = pd.DataFrame()
    for _role in all_roles:
        q_against = pd.concat([q_against, pd.DataFrame(run_query(champion_matchup_query(
            patches, phases, teams, roles, tournaments, champion, role=_role, maps=maps, selected_roles=selected_roles)),
            columns=['Pick', 'Role', 'Qty Pick', 'Qty Win']
        )])
        q_with = pd.concat([q_with, pd.DataFrame(run_query(champion_matchup_query(
            patches, phases, teams, roles, tournaments, champion, role=_role, maps=maps, against=False, selected_roles=selected_roles)),
            columns=['Pick', 'Role', 'Qty Pick', 'Qty Win']
        )])
    q_with['%WR'] = (q_with['Qty Win'] / q_with['Qty Pick']) * 100
    q_against['%WR'] = (q_against['Qty Win'] / q_against['Qty Pick']) * 100
    with col1:
        st.title('Played With')
        st.dataframe(q_with.style.format(precision=2))
    with col2:
        st.title('Played Against')
        st.dataframe(q_against.style.format(precision=2))

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
    player_df.style.format(precision=2)
    st.dataframe(
        player_df.style.format(precision=2).format(subset=[*INT_COLUMNS, *INDIVIDUAL_COLUMNS],
                                                   formatter='{:.0f}'), height=550)
