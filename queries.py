import pandas as pd

picks_bans_df = pd.read_csv('https://docs.google.com/spreadsheets/d/1lBgkZfa7hakVNY26wmhdLqgtqFwX0t8NTqjpL1YVMSo/export?format=csv&gid=1324570847')
match_stats_df = pd.read_csv('https://docs.google.com/spreadsheets/d/1lBgkZfa7hakVNY26wmhdLqgtqFwX0t8NTqjpL1YVMSo/export?format=csv&gid=1709316147')
champion_df = pd.read_csv('champion.csv')

TOURNAMENT_QUERY = "SELECT DISTINCT tournament from picks_bans_df"
PATCHES_QUERY = "SELECT DISTINCT patch FROM picks_bans_df WHERE patch is not null"
PHASES_QUERY = "SELECT DISTINCT phase FROM picks_bans_df"
TEAM_QUERY = "SELECT DISTINCT team_tag FROM picks_bans_df"
ROLE_QUERY = "SELECT DISTINCT role FROM picks_bans_df"
CHAMPION_ROLE_QUERY = "SELECT DISTINCT pick, role FROM picks_bans_df ORDER BY pick"


def format_tournament_tuple(tournaments):
    return '", "'.join(tournaments)


def format_role_coluns_tuple(roles):
    return ', '.join([f'{r}_pick' for r in roles])


def role_query(champion):
    return f"SELECT DISTINCT role FROM picks_bans_df WHERE pick = '{champion}'"


def champion_matchup_query(
        patches=None, phases=None, teams=None, tournaments=None,
        champion=None, player=None, role=None, maps=None, against=True):

    if tournaments is None:
        tournaments = []
    if teams is None:
        teams = []
    if phases is None:
        phases = []
    if patches is None:
        patches = []
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
        _ = len(patches) + len(phases)
        where_clause = f"{where_clause} " \
                       f"{'AND' if _ > 0 else ''}" \
                       f" team_tag = '{teams[0]}'"
    if len(teams) > 1:
        _ = len(patches) + len(phases)
        where_clause = f"{where_clause} " \
                       f"{'AND' if _ > 0 else ''}" \
                       f" team_tag IN {tuple(teams)}"
    if len(tournaments) == 1:
        _ = len(patches) + len(phases) + len(teams)
        where_clause = f"{where_clause} " \
                       f"{'AND' if _ > 0 else ''}" \
                       f' tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        _ = len(patches) + len(phases) + len(teams)
        where_clause = f"{where_clause} " \
                       f"{'AND' if _ > 0 else ''}" \
                       f' tournament IN ("{format_tournament_tuple(tournaments)}")'
    if len(maps) == 1:
        _ = len(patches) + len(phases) + len(teams) + len(tournaments)
        where_clause = f"{where_clause} " \
                       f"{'AND' if _ > 0 else ''}" \
                       f' map_id = "{maps[0]}"'
    if len(maps) > 1:
        _ = len(patches) + len(phases) + len(teams) + len(tournaments)
        where_clause = f"{where_clause} " \
                       f"{'AND' if _ > 0 else ''}" \
                       f' map_id IN {tuple(maps)}'
    if player is not None:
        _ = len(patches) + len(phases) + len(teams) + len(tournaments)
        where_clause = f"{where_clause} " \
                       f"{'AND' if _ > 0 else ''}" \
                       f' {role}_player = "{player}"'
    if against:
        _ = len(patches) + len(phases) + len(teams) + len(tournaments)
        where_clause = f"{where_clause} " \
                       f"{'AND' if _ > 0 or champion is not None else ''}" \
                       f' "{champion}" NOT IN (baron_pick, jungle_pick, mid_pick, dragon_pick, sup_pick)'
    else:
        _ = len(patches) + len(phases) + len(teams) + len(tournaments)
        where_clause = f"{where_clause} " \
                       f"{'AND' if _ > 0 or champion is not None else ''}" \
                       f' "{champion}" != {role}_pick AND ' \
                       f' "{champion}" IN (baron_pick, jungle_pick, mid_pick, dragon_pick, sup_pick)'
    return f"""-- {'against' if against else 'with'}
        SELECT 
           {role}_pick AS pick,
           '{role}' AS role,
           COUNT({role}_pick) AS qty_pick,
           SUM({'NOT' if against else ''} winner) as qty_win
        FROM match_stats_df {where_clause if where_clause != 'WHERE' else ''}
        GROUP BY {role}_pick"""


def players_query(patches=None, phases=None, teams=None, roles=None, tournaments=None):

    if tournaments is None:
        tournaments = []
    if roles is None:
        roles = []
    if teams is None:
        teams = []
    if phases is None:
        phases = []
    if patches is None:
        patches = []
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
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag = '{teams[0]}'"
    if len(teams) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag IN {tuple(teams)}"
    if len(roles) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f" role = '{roles[0]}'"
    if len(roles) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f" role IN {tuple(roles)}"
    if len(tournaments) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) > 0 else ''}" \
                       f' tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) > 0 else ''}" \
                       f' tournament IN ("{format_tournament_tuple(tournaments)}")'

    return f"SELECT DISTINCT player FROM picks_bans_df {where_clause if where_clause != 'WHERE' else ''}"


def champion_maps_query(
        patches=None, phases=None, teams=None, roles=None, tournaments=None,
        champion=None, player=None):

    if tournaments is None:
        tournaments = []
    if roles is None:
        roles = []
    if teams is None:
        teams = []
    if phases is None:
        phases = []
    if patches is None:
        patches = []
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
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag = '{teams[0]}'"
    if len(teams) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag IN {tuple(teams)}"
    if len(roles) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f" role = '{roles[0]}'"
    if len(roles) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f" role IN {tuple(roles)}"
    if len(tournaments) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) > 0 else ''}" \
                       f' tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) > 0 else ''}" \
                       f' tournament IN ("{format_tournament_tuple(tournaments)}")'
    if champion is not None:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) + len(tournaments) > 0 else ''}" \
                       f' pick = "{champion}"'
    if player is not None:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) + len(tournaments) > 0 else ''}" \
                       f' player = "{player}"'

    return f"SELECT DISTINCT map_id FROM picks_bans_df {where_clause if where_clause != 'WHERE' else ''}"


def total_games_query(patches=None, phases=None, teams=None, tournaments=None):
    if tournaments is None:
        tournaments = []
    if teams is None:
        teams = []
    if phases is None:
        phases = []
    if patches is None:
        patches = []
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
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag = '{teams[0]}'"
    if len(teams) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag IN {tuple(teams)}"
    if len(tournaments) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f' tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f' tournament IN ("{format_tournament_tuple(tournaments)}")'
    return f"""
        SELECT COUNT(map_id) / 2 FROM match_stats_df {where_clause if where_clause != 'WHERE' else ''}
    """


def presence_query(patches=None, phases=None, teams=None, tournaments=None, pick_ban='pick'):
    if tournaments is None:
        tournaments = []
    if teams is None:
        teams = []
    if phases is None:
        phases = []
    if patches is None:
        patches = []
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
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag = '{teams[0]}'"
    if len(teams) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag IN {tuple(teams)}"
    if len(tournaments) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f' tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f' tournament IN ("{format_tournament_tuple(tournaments)}")'
    return f"""
        SELECT 
            {pick_ban}, role, COUNT({pick_ban}) AS qty_{pick_ban}, SUM(winner) AS qty_win
        FROM picks_bans_df {where_clause if where_clause != 'WHERE' else ''}
        GROUP BY {pick_ban}, role
        ORDER BY {pick_ban}
    """


def picks_bans_query(patches=None, phases=None, teams=None, tournaments=None, pick_ban='pick', side='blue'):
    if tournaments is None:
        tournaments = []
    if teams is None:
        teams = []
    if phases is None:
        phases = []
    if patches is None:
        patches = []
    where_clause = f"WHERE side = '{side}'"
    if len(patches) == 1:
        where_clause = f"{where_clause} AND patch = '{patches[0]}'"
    if len(patches) > 1:
        where_clause = f"{where_clause} AND patch IN {tuple(patches)}"
    if len(phases) == 1:
        where_clause = f"{where_clause}  AND phase = '{phases[0]}'"
    if len(phases) > 1:
        where_clause = f"{where_clause} AND phase IN {tuple(phases)}"
    if len(teams) == 1:
        where_clause = f"{where_clause} AND team_tag = '{teams[0]}'"
    if len(teams) > 1:
        where_clause = f"{where_clause} AND team_tag IN {tuple(teams)}"
    if len(tournaments) == 1:
        where_clause = f'{where_clause} AND tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        where_clause = f'{where_clause} AND tournament IN ("{format_tournament_tuple(tournaments)}")'
    return f"""
        SELECT 
            {pick_ban},
            {pick_ban}_rotation,
            COUNT({pick_ban}) AS qty_{pick_ban},
            SUM(winner) as qty_win
        FROM picks_bans_df
        {where_clause if where_clause != 'WHERE' else f"WHERE side = '{side}'"}
        GROUP BY {pick_ban}, {pick_ban}_rotation, side
        ORDER BY side, {pick_ban}_rotation, COUNT({pick_ban}) DESC, {pick_ban}
    """


def prio_query(patches=None, phases=None, teams=None, tournaments=None):
    if tournaments is None:
        tournaments = []
    if teams is None:
        teams = []
    if phases is None:
        phases = []
    if patches is None:
        patches = []
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
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag = '{teams[0]}'"
    if len(teams) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag IN {tuple(teams)}"
    if len(tournaments) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f' tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f' tournament IN ("{format_tournament_tuple(tournaments)}")'
    return f"""
        SELECT
            side, 
            pick_rotation, 
            role, 
            COUNT(role) AS total, 
            SUM(winner) AS total_win
        FROM picks_bans_df {where_clause if where_clause != 'WHERE' else ''}
        GROUP BY side, pick_rotation, role
        ORDER BY side, pick_rotation, role DESC
    """


def blind_response_query(patches=None, phases=None, teams=None, tournaments=None):
    if tournaments is None:
        tournaments = []
    if teams is None:
        teams = []
    if phases is None:
        phases = []
    if patches is None:
        patches = []
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
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag = '{teams[0]}'"
    if len(teams) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag IN {tuple(teams)}"
    if len(tournaments) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f' tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f' tournament IN ("{format_tournament_tuple(tournaments)}")'
    return f"""
        SELECT
            side, 
            pick_rotation, 
            role, 
            SUM(is_blind) AS total_blind, 
            SUM(is_blind AND winner) AS win_blind, 
            SUM(is_blind = false) AS total_response, 
            SUM(is_blind = false AND winner) AS win_response
        FROM picks_bans_df {where_clause if where_clause != 'WHERE' else ''}
        GROUP BY side, pick_rotation, role
        ORDER BY side, pick_rotation, role DESC
    """


def patches_query(tournaments=None):
    if tournaments is None:
        tournaments = []

    if len(tournaments) == 1:
        return f'{PATCHES_QUERY} AND tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        return f'{PATCHES_QUERY} AND tournament IN ("{format_tournament_tuple(tournaments)}")'
    return PATCHES_QUERY


def phases_query(tournaments=None):
    if tournaments is None:
        tournaments = []

    if len(tournaments) == 1:
        return f'{PHASES_QUERY} WHERE tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        return f'{PHASES_QUERY} WHERE tournament IN ("{format_tournament_tuple(tournaments)}")'
    return PHASES_QUERY


def teams_query(tournaments=None):
    if tournaments is None:
        tournaments = []

    if len(tournaments) == 1:
        return f'{TEAM_QUERY} WHERE tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        return f'{TEAM_QUERY} WHERE tournament IN ("{format_tournament_tuple(tournaments)}")'
    return TEAM_QUERY


def general_stats_query(
        patches=None, phases=None, teams=None, roles=None, tournaments=None,
        columns='pick', is_team=False, df='picks_bans_df', champion=None, player=None):

    if tournaments is None:
        tournaments = []
    if roles is None:
        roles = []
    if teams is None:
        teams = []
    if phases is None:
        phases = []
    if patches is None:
        patches = []
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
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag = '{teams[0]}'"
    if len(teams) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) > 0 else ''}" \
                       f" team_tag IN {tuple(teams)}"
    if len(roles) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f" role = '{roles[0]}'"
    if len(roles) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) > 0 else ''}" \
                       f" role IN {tuple(roles)}"
    if len(tournaments) == 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) > 0 else ''}" \
                       f' tournament = "{tournaments[0]}"'
    if len(tournaments) > 1:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) > 0 else ''}" \
                       f' tournament IN ("{format_tournament_tuple(tournaments)}")'
    if champion is not None:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) + len(tournaments) > 0 else ''}" \
                       f" pick = '{champion}'"
    if player is not None:
        where_clause = f"{where_clause} " \
                       f"{'AND' if len(patches) + len(phases) + len(teams) + len(roles) + len(tournaments) > 0 else ''}" \
                       f' player = "{player}"'

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
            SELECT {columns}, {individual_stats if not is_team else ''}
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
