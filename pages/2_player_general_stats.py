from shillelagh.backends.apsw.db import connect
import streamlit as st
import pandas as pd
import numpy as np

connection = connect(':memory:')
cursor = connection.cursor()
my_df = pd.read_csv('https://wrflask.dinossauro.dev/v1/download/picks_bans?t=7&winner_loser=binary&blind_response=binary&pick_rotation=explicit_eng')

st.set_page_config(layout="wide")

st.title("Player general stats")
INT_COLUMNS = ['AVG DDPM', 'AVG DTPM', 'AVG GPM']
TIME_COLUMNS = ['AGT', 'AGT Win', 'AGT Loss']
PATCHES_QUERY = "SELECT DISTINCT patch FROM my_df"
PHASES_QUERY = "SELECT DISTINCT phase FROM my_df"
TEAM_QUERY = "SELECT DISTINCT team_tag FROM my_df"
ROLE_QUERY = "SELECT DISTINCT role FROM my_df"


def general_stats_query():
    where_clause = 'WHERE'
    if len(patches) == 1:
        where_clause = f"{where_clause} patch = '{patches[0]}'"
    if len(patches) > 1:
        where_clause = f"{where_clause} patch IN {tuple(patches)}"
    if len(phases) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) > 0 else ''}" \
                       f" phase = '{phases[0]}'"
    if len(phases) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) > 0 else ''}" \
                       f" phase IN {tuple(phases)}"
    if len(teams) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) > 0 or len(phases) > 0 else ''}" \
                       f" team_tag = '{teams[0]}'"
    if len(teams) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) > 0 or len(phases) > 0 else ''}" \
                       f" team_tag IN {tuple(teams)}"
    if len(roles) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) > 0 or len(phases) > 0 or len(teams) > 0 else ''}" \
                       f" role = '{roles[0]}'"
    if len(roles) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) > 0 or len(phases) > 0 or len(teams) > 0 else ''}" \
                       f" role IN {tuple(roles)}"
    return f"""
        SELECT 
            role,
            player, 
            ROUND(AVG(kills), 2) AS avg_kills, 
            ROUND(AVG(deaths), 2) AS avg_deaths, 
            ROUND(AVG(assists), 2) AS avg_assists,
            ROUND((AVG(kills) + AVG(assists)) / AVG(assists), 0) AS avg_kda,
            ROUND(AVG(dmg_dealt) / (AVG(length_sec) / 60), 0) AS avg_ddpm,
            ROUND(AVG(dmg_taken) / (AVG(length_sec) / 60), 0) AS avg_dtpm,
            ROUND(AVG(total_gold) / (AVG(length_sec) / 60), 0) AS avg_gold,
            ROUND(AVG(dmg_dealt) / AVG(total_gold), 2) AS avg_ddpg,
            ROUND(AVG(dmg_taken) / AVG(total_gold), 2) AS avg_dtpg,
            ROUND(AVG(length_sec), 0) AS AGT,
            ROUND(AVG(
                CASE winner
                    WHEN true THEN length_sec
                    ELSE null
                END
            ), 0) AS AGT_WIN,
            ROUND(AVG(
                CASE winner
                    WHEN false THEN length_sec
                    ELSE null
                END
            ), 0) AS AGT_LOSS
        FROM my_df
        {where_clause if where_clause != 'WHERE' else ''}
        GROUP BY role, player
    """


@st.cache(ttl=600)
def run_query(query):
    rows = cursor.execute(query)
    return rows.fetchall()


patches = st.sidebar.multiselect('Patch', sum(run_query(PATCHES_QUERY), ()))
phases = st.sidebar.multiselect('Fase', sum(run_query(PHASES_QUERY), ()))
teams = st.sidebar.multiselect('Time', sum(run_query(TEAM_QUERY), ()))
roles = st.sidebar.multiselect('Role', sum(run_query(ROLE_QUERY), ()))

other_df = pd.DataFrame(run_query(general_stats_query()), columns=[
    'Role', 'Player', 'AVG Kills', 'AVG Deaths', 'AVG Assists', 'AVG KDA',
    'AVG DDPM', 'AVG DTPM', 'AVG GPM', 'AVG DDPG', 'AVG DTPG', 'AGT', 'AGT Win', 'AGT Loss'
])
for colum in TIME_COLUMNS:
    other_df[colum] = pd.to_datetime(other_df[colum], unit='s').dt.strftime("%M:%S")
    other_df[colum] = other_df[colum].replace(np.nan, '-')
other_df['AVG KDA'] = (other_df['AVG Kills'] + other_df['AVG Assists']) / other_df['AVG Deaths']
other_df['DDPG'] = other_df['AVG DDPM'] / other_df['AVG GPM']
other_df['DTPG'] = other_df['AVG DTPM'] / other_df['AVG GPM']
other_df.style.format(precision=2)
st.dataframe(other_df.style.format(precision=2).format(subset=INT_COLUMNS, formatter='{:.0f}'), height=550)
