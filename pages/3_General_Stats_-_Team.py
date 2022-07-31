from datetime import timedelta
from shillelagh.backends.apsw.db import connect
from queries import PATCHES_QUERY, PHASES_QUERY, general_stats_query
import streamlit as st
import pandas as pd
import numpy as np

connection = connect(':memory:')
cursor = connection.cursor()
my_df = pd.read_csv(
    'https://wrflask.dinossauro.dev/v1/download/match_stats'
    '?t=7&winner_loser=binary&blind_response=binary&pick_rotation=explicit_eng'
)

st.set_page_config(layout="wide")

st.title("Team general stats")
INT_COLUMNS = ['QTY Games', 'QTY Blue', 'QTY Red']
TIME_COLUMNS = ['AGT', 'AGT Win', 'AGT Loss']


@st.cache(ttl=600)
def run_query(query):
    rows = cursor.execute(query)
    return rows.fetchall()


patches = st.sidebar.multiselect('Patch', sum(run_query(PATCHES_QUERY), ()))
phases = st.sidebar.multiselect('Fase', sum(run_query(PHASES_QUERY), ()))

other_df = pd.DataFrame(run_query(general_stats_query(patches=patches, phases=phases, columns='team_name, team_tag', is_team=True)), columns=[
    'team', 'tag', 'QTY Games', '%WR', 'QTY Blue', '%WR Blue', 'QTY Red', '%WR Red', 'AGT', 'AGT Win', 'AGT Loss'
])
other_df['%WR'] = (other_df['%WR'] / other_df['QTY Games']) * 100
other_df['%WR Blue'] = (other_df['%WR Blue'] / other_df['QTY Blue']) * 100
other_df['%WR Red'] = (other_df['%WR Red'] / other_df['QTY Red']) * 100
agt = other_df['AGT'].mean()
agt = str(timedelta(seconds=agt)).split(':')
agt = f'{agt[1]}:{agt[2][:2]}'
for colum in TIME_COLUMNS:
    other_df[colum] = pd.to_datetime(other_df[colum], unit='s').dt.strftime("%M:%S")
    other_df[colum] = other_df[colum].replace(np.nan, '-')
col1, col2, col3 = st.columns(3, gap='small')
with col1:
    st.metric('QTY Games', len(other_df) / 2)
with col2:
    st.metric('AGT', agt)
with col3:
    st.metric('AVG Games', round(other_df['QTY Games'].mean(), 2))
other_df.style.format(precision=2)
st.dataframe(other_df.style.format(precision=2).format(subset=INT_COLUMNS, formatter='{:.0f}'))
