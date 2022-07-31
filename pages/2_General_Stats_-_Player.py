from datetime import timedelta

from shillelagh.backends.apsw.db import connect
from queries import PATCHES_QUERY, PHASES_QUERY, TEAM_QUERY, ROLE_QUERY, general_stats_query
import streamlit as st
import pandas as pd
import numpy as np

connection = connect(':memory:')
cursor = connection.cursor()
my_df = pd.read_csv(
    'https://wrflask.dinossauro.dev/v1/download/picks_bans'
    '?t=7&winner_loser=binary&blind_response=binary&pick_rotation=explicit_eng'
)

st.set_page_config(layout="wide")

st.title("Player general stats")
INT_COLUMNS = ['AVG DDPM', 'AVG DTPM', 'AVG GPM']
TIME_COLUMNS = ['AGT', 'AGT Win', 'AGT Loss']


@st.cache(ttl=600)
def run_query(query):
    rows = cursor.execute(query)
    return rows.fetchall()


patches = st.sidebar.multiselect('Patch', sum(run_query(PATCHES_QUERY), ()))
phases = st.sidebar.multiselect('Fase', sum(run_query(PHASES_QUERY), ()))
teams = st.sidebar.multiselect('Time', sum(run_query(TEAM_QUERY), ()))
roles = st.sidebar.multiselect('Role', sum(run_query(ROLE_QUERY), ()))

other_df = pd.DataFrame(run_query(general_stats_query(patches, phases, teams, roles, 'role, player')), columns=[
    'Role', 'Player', 'AVG Kills', 'AVG Deaths', 'AVG Assists', 'AVG KDA',
    'AVG DDPM', 'AVG DTPM', 'AVG GPM', 'AVG DDPG', 'AVG DTPG',
    'QTY Games', '%WR', 'QTY Blue', '%WR Blue', 'QTY Red', '%WR Red',
    'AGT', 'AGT Win', 'AGT Loss'
])
agt = other_df['AGT'].mean()
agt = str(timedelta(seconds=agt)).split(':')
agt = f'{agt[1]}:{agt[2][:2]}'
for colum in TIME_COLUMNS:
    other_df[colum] = pd.to_datetime(other_df[colum], unit='s').dt.strftime("%M:%S")
    other_df[colum] = other_df[colum].replace(np.nan, '-')
other_df['AVG KDA'] = (other_df['AVG Kills'] + other_df['AVG Assists']) / other_df['AVG Deaths']
other_df['DDPG'] = other_df['AVG DDPM'] / other_df['AVG GPM']
other_df['DTPG'] = other_df['AVG DTPM'] / other_df['AVG GPM']
other_df.style.format(precision=2)
other_df.style.format(precision=2)
col1, col2, col3 = st.columns(3, gap='small')
with col1:
    st.metric('AVG Games', round(other_df['QTY Games'].mean(), 2))
with col2:
    st.metric('AGT', agt)
with col3:
    st.metric('AVG Games', round(other_df['QTY Games'].mean(), 2))
st.dataframe(other_df.style.format(precision=2).format(subset=INT_COLUMNS, formatter='{:.0f}'), height=550)
