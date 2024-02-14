from shillelagh.backends.apsw.db import connect
import pandas as pd

connection = connect(':memory:')
cursor = connection.cursor()

csv_url = 'files/match_stats.csv'
my_df = pd.read_csv(csv_url)
PATCHES_QUERY = "SELECT DISTINCT patch FROM my_df"
PHASES_QUERY = "SELECT DISTINCT phase FROM my_df"
sql = """
    SELECT
        baron_pick AS pick,
        'baron' AS role,
        COUNT(baron_pick) AS qty_match,
        SUM(winner) AS qty_win
    FROM my_df
    WHERE
        baron_pick != 'Ahri' AND
        'Ahri' IN (baron_pick, mid_pick)
    GROUP BY baron_pick
    UNION ALL
    SELECT
        jungle_pick AS pick,
        'jungle' AS role,
        COUNT(jungle_pick) AS qty_match,
        SUM(winner) AS qty_win
    FROM my_df
    WHERE
        baron_pick != 'Ahri' AND
        'Ahri' IN (baron_pick, mid_pick)
    GROUP BY baron_pick
    ORDER BY qty_match, qty_win
"""

other_df = pd.DataFrame(cursor.execute(sql).fetchall(), columns=[
    'Pick', 'Role', 'Qty Match', 'Qty Win'
])
print(other_df)