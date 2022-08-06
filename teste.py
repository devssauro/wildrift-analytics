from shillelagh.backends.apsw.db import connect
import pandas as pd

connection = connect(':memory:')
cursor = connection.cursor()

csv_url = 'https://wrflask.dinossauro.dev/v1/download/match_stats?winner_loser=binary&blind_response=binary&pick_rotation=explicit_eng'
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
        'Ahri' IN (baron_pick, mid_pick) AND
        map_id IN (1, 22, 24, 8, 9, 13, 16, 30, 18, 60, 103, 123, 144, 155, 162, 171, 180, 183, 191, 209)
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
        'Ahri' IN (baron_pick, mid_pick) AND
        map_id IN (1, 22, 24, 8, 9, 13, 16, 30, 18, 60, 103, 123, 144, 155, 162, 171, 180, 183, 191, 209)
    GROUP BY baron_pick
    ORDER BY qty_match, qty_win
"""

other_df = pd.DataFrame(cursor.execute(sql).fetchall(), columns=[
    'Pick', 'Role', 'Qty Match', 'Qty Win'
])
print(other_df)