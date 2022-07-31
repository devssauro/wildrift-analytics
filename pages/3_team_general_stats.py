from shillelagh.backends.apsw.db import connect
import streamlit as st
import pandas as pd
import numpy as np

connection = connect(':memory:')
cursor = connection.cursor()
my_df = pd.read_csv('https://wrflask.dinossauro.dev/v1/download/match_stats?t=7&winner_loser=binary&blind_response=binary&pick_rotation=explicit_eng')

st.set_page_config(layout="wide")

st.title("Team general stats")
INT_COLUMNS = ['QTY Games', 'QTY Blue', 'QTY Red']
TIME_COLUMNS = ['AGT', 'AGT Win', 'AGT Loss']
PATCHES_QUERY = "SELECT DISTINCT patch FROM my_df"
PHASES_QUERY = "SELECT DISTINCT phase FROM my_df"


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
    return f"""
        SELECT 
            team_name,
            team_tag,
            COUNT(team_tag) AS qty_games,
            SUM(winner) AS qty_win,
            SUM(side = 'blue') AS qty_blue,
            SUM(side = 'blue' AND winner) AS win_blue,
            SUM(side = 'red') AS qty_red,
            SUM(side = 'red' AND winner) AS win_red,
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
        GROUP BY team_name, team_tag
    """


@st.cache(ttl=600)
def run_query(query):
    rows = cursor.execute(query)
    return rows.fetchall()


patches = st.sidebar.multiselect('Patch', sum(run_query(PATCHES_QUERY), ()))
phases = st.sidebar.multiselect('Fase', sum(run_query(PHASES_QUERY), ()))

other_df = pd.DataFrame(run_query(general_stats_query()), columns=[
    'team', 'tag', 'QTY Games', '%WR', 'QTY Blue', '%WR Blue', 'QTY Red', '%WR Red', 'AGT', 'AGT Win', 'AGT Loss'
])
other_df['%WR'] = (other_df['%WR'] / other_df['QTY Games']) * 100
other_df['%WR Blue'] = (other_df['%WR Blue'] / other_df['QTY Blue']) * 100
other_df['%WR Red'] = (other_df['%WR Red'] / other_df['QTY Red']) * 100
for colum in TIME_COLUMNS:
    other_df[colum] = pd.to_datetime(other_df[colum], unit='s').dt.strftime("%M:%S")
    other_df[colum] = other_df[colum].replace(np.nan, '-')
other_df.style.format(precision=2)
st.dataframe(other_df.style.format(precision=2).format(subset=INT_COLUMNS, formatter='{:.0f}'))
