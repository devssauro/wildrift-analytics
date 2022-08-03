from shillelagh.backends.apsw.db import connect
import pandas as pd

connection = connect(':memory:')
cursor = connection.cursor()

csv_url = 'https://wrflask.dinossauro.dev/v1/download/picks_bans?t=7&winner_loser=binary&blind_response=binary&pick_rotation=explicit_eng'
PATCHES_QUERY = "SELECT DISTINCT patch FROM my_df"
PHASES_QUERY = "SELECT DISTINCT phase FROM my_df"
sql = """
    SELECT 
        pick, 
        ROUND(AVG(kills), 2) AS avg_kills, 
        ROUND(AVG(deaths), 2) AS avg_deaths, 
        ROUND(AVG(assists), 2) AS avg_assists,
        ROUND((AVG(kills) + AVG(assists)) / AVG(assists), 0) AS avg_kda,
        ROUND(AVG(dmg_dealt) / (AVG(length_sec) / 60), 0) AS avg_ddpm,
        ROUND(AVG(dmg_taken) / (AVG(length_sec) / 60), 0) AS avg_dtpm,
        ROUND(AVG(total_gold) / (AVG(length_sec) / 60), 0) AS avg_gold,
        ROUND(AVG(dmg_dealt) / AVG(total_gold), 0) AS avg_ddpg,
        ROUND(AVG(length_sec), 0) AS AGT
    FROM my_df
    GROUP BY pick
"""

other_df = pd.DataFrame(cursor.execute(sql).fetchall(), columns=[
    'pick', 'AVG Kills', 'AVG Deaths', 'AVG Assists', 'AVG KDA',
    'AVG DDPM', 'AVG DTPM', 'AVG GPM', 'AVG DDPG', 'AGT'
])

print(sum(cursor.execute(PATCHES_QUERY).fetchall(), ()))
print(sum(cursor.execute(PHASES_QUERY).fetchall(), ()))

prio_role[row.side][row.pick_rotation][row.role] = row.total
wr_role[row.side][row.pick_rotation][row.role] = row.total_win
for side in prio_role.keys():
    for rotation in prio_role[side].keys():
        final_list.append({
            'side': side,
            'rotation': rotation,
            'baron': prio_percent(
                prio_role[side][rotation].get('baron', 0), total_games[side], side, rotation),
            'jungle': prio_percent(
                prio_role[side][rotation].get('jungle', 0), total_games[side], side, rotation),
            'mid': prio_percent(
                prio_role[side][rotation].get('mid', 0), total_games[side], side, rotation),
            'dragon': prio_percent(
                prio_role[side][rotation].get('dragon', 0), total_games[side], side, rotation),
            'sup': prio_percent(
                prio_role[side][rotation].get('sup', 0), total_games[side], side, rotation)
        })
        wr_list.append({
            'side': side,
            'rotation': rotation,
            'baron': prio_percent_wr(
                prio_role[side][rotation].get('baron', 0), wr_role[side][rotation].get('baron', 0), side, rotation,
                'baron'),
            'jungle': prio_percent_wr(
                prio_role[side][rotation].get('jungle', 0), wr_role[side][rotation].get('jungle', 0), side,
                rotation, 'jungle'),
            'mid': prio_percent_wr(
                prio_role[side][rotation].get('mid', 0), wr_role[side][rotation].get('mid', 0), side, rotation,
                'mid'),
            'dragon': prio_percent_wr(
                prio_role[side][rotation].get('dragon', 0), wr_role[side][rotation].get('dragon', 0), side,
                rotation, 'dragon'),
            'sup': prio_percent_wr(
                prio_role[side][rotation].get('sup', 0), wr_role[side][rotation].get('sup', 0), side, rotation,
                'sup')
        })
pr_df = pd.DataFrame(final_list)
wr_df = pd.DataFrame(wr_list)

pr_df.style.format(precision=2)
wr_df.style.format(precision=2)
