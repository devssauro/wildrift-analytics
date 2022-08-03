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


general_tab, picks_tab, bans_tab, presence_tab = st.tabs(["Geral", "Picks", "Bans", "Prsença"])

tournaments = st.sidebar.multiselect(
    'Campeonatos', sum(run_query(TOURNAMENT_QUERY), ()),)
#patches = st.sidebar.multiselect('Patch', sum(run_query(patches_query(tournaments)), ()))
#phases = st.sidebar.multiselect('Fase', sum(run_query(phases_query(tournaments)), ()))
#teams = st.sidebar.multiselect('Time', sum(run_query(teams_query(tournaments)), ()))
#roles = st.sidebar.multiselect('Role', sum(run_query(ROLE_QUERY), ()))

with general_tab:
    col1, col2 = st.columns(2)
    st.write(run_query(teams_query(tournaments)))
    # Pick rate and Win Rate
    #st.write(prio_query(patches=patches, phases=phases, tournaments=tournaments))
    #st.write(blind_response_query(patches=patches, phases=phases, tournaments=tournaments))
