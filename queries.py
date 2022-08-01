PATCHES_QUERY = "SELECT DISTINCT patch FROM individual_df"
PHASES_QUERY = "SELECT DISTINCT phase FROM individual_df"
TEAM_QUERY = "SELECT DISTINCT team_tag FROM individual_df"
ROLE_QUERY = "SELECT DISTINCT role FROM individual_df"


def general_stats_query(patches=[], phases=[], teams=[], roles=[], columns='pick', is_team=False, df='individual_df'):
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
    individual_stats = """
        ROUND(AVG(kills), 2) AS avg_kills, 
        ROUND(AVG(deaths), 2) AS avg_deaths, 
        ROUND(AVG(assists), 2) AS avg_assists,
        ROUND((AVG(kills) + AVG(assists)) / AVG(assists), 0) AS avg_kda,
        ROUND(AVG(dmg_dealt) / (AVG(length_sec) / 60), 0) AS avg_ddpm,
        ROUND(AVG(dmg_taken) / (AVG(length_sec) / 60), 0) AS avg_dtpm,
        ROUND(AVG(total_gold) / (AVG(length_sec) / 60), 0) AS avg_gold,
        ROUND(AVG(dmg_dealt) / AVG(total_gold), 2) AS avg_ddpg,
        ROUND(AVG(dmg_taken) / AVG(total_gold), 2) AS avg_dtpg,
    """
    return f"""
            SELECT 
                {columns},
                {individual_stats if not is_team else ''}
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
            FROM {df}
            {where_clause if where_clause != 'WHERE' else ''}
            GROUP BY {columns}
        """
