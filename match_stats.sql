SELECT
    GENERATE_UUID() AS id,
    id AS map_id,
    matchup_id,
    tournament,
    map_number,
    patch,
    phase,
    blue_side_tag AS team_tag,
    blue_side_team AS team_name,
    'blue' AS side,
    length,
    length_sec,
    winner = blue_side_tag AS winner,
    winner_side,
    blue_ban_1 AS ban_1,
    blue_ban_2 AS ban_2,
    blue_ban_3 AS ban_3,
    blue_ban_4 AS ban_4,
    blue_ban_5 AS ban_5,
    blue_pick_1 AS pick_1,
    blue_pick_2 AS pick_2,
    blue_pick_3 AS pick_3,
    blue_pick_4 AS pick_4,
    blue_pick_5 AS pick_5,
    blue_baron_pick AS baron_pick,
    blue_jungle_pick AS jungle_pick,
    blue_mid_pick AS mid_pick,
    blue_dragon_pick AS dragon_pick,
    blue_sup_pick AS sup_pick,
    blue_baron_kills AS baron_kills,
    blue_jungle_kills AS jungle_kills,
    blue_mid_kills AS mid_kills,
    blue_dragon_kills AS dragon_kills,
    blue_sup_kills AS sup_kills,
    blue_baron_deaths AS baron_deaths,
    blue_jungle_deaths AS jungle_deaths,
    blue_mid_deaths AS mid_deaths,
    blue_dragon_deaths AS dragon_deaths,
    blue_sup_deaths AS sup_deaths,
    blue_baron_assists AS baron_assists,
    blue_jungle_assists AS jungle_assists,
    blue_mid_assists AS mid_assists,
    blue_dragon_assists AS dragon_assists,
    blue_sup_assists AS sup_assists,
    blue_baron_dmg_taken AS baron_dmg_taken,
    blue_jungle_dmg_taken AS jungle_dmg_taken,
    blue_mid_dmg_taken AS mid_dmg_taken,
    blue_dragon_dmg_taken AS dragon_dmg_taken,
    blue_sup_dmg_taken AS sup_dmg_taken,
    blue_baron_dmg_dealt AS baron_dmg_dealt,
    blue_jungle_dmg_dealt AS jungle_dmg_dealt,
    blue_mid_dmg_dealt AS mid_dmg_dealt,
    blue_dragon_dmg_dealt AS dragon_dmg_dealt,
    blue_sup_dmg_dealt AS sup_dmg_dealt,
    blue_baron_total_gold AS baron_total_gold,
    blue_jungle_total_gold AS jungle_total_gold,
    blue_mid_total_gold AS mid_total_gold,
    blue_dragon_total_gold AS dragon_total_gold,
    blue_sup_total_gold AS sup_total_gold,
    blue_baron_player AS baron_player,
    blue_jungle_player AS jungle_player,
    blue_mid_player AS mid_player,
    blue_dragon_player AS dragon_player,
    blue_sup_player AS sup_player
FROM map_data.maps
UNION ALL
SELECT
    GENERATE_UUID() AS id,
    id AS map_id,
    matchup_id,
    tournament,
    map_number,
    patch,
    phase,
    red_side_tag AS team_id,
    red_side_team AS team_name,
    'red' AS side,
    length,
    length_sec,
    winner = red_side_tag AS winner,
    winner_side,
    red_ban_1 AS ban_1,
    red_ban_2 AS ban_2,
    red_ban_3 AS ban_3,
    red_ban_4 AS ban_4,
    red_ban_5 AS ban_5,
    red_pick_1 AS pick_1,
    red_pick_2 AS pick_2,
    red_pick_3 AS pick_3,
    red_pick_4 AS pick_4,
    red_pick_5 AS pick_5,
    red_baron_pick AS baron_pick,
    red_jungle_pick AS jungle_pick,
    red_mid_pick AS mid_pick,
    red_dragon_pick AS dragon_pick,
    red_sup_pick AS sup_pick,
    red_baron_kills AS baron_kills,
    red_jungle_kills AS jungle_kills,
    red_mid_kills AS mid_kills,
    red_dragon_kills AS dragon_kills,
    red_sup_kills AS sup_kills,
    red_baron_deaths AS baron_deaths,
    red_jungle_deaths AS jungle_deaths,
    red_mid_deaths AS mid_deaths,
    red_dragon_deaths AS dragon_deaths,
    red_sup_deaths AS sup_deaths,
    red_baron_assists AS baron_assists,
    red_jungle_assists AS jungle_assists,
    red_mid_assists AS mid_assists,
    red_dragon_assists AS dragon_assists,
    red_sup_assists AS sup_assists,
    red_baron_dmg_taken AS baron_dmg_taken,
    red_jungle_dmg_taken AS jungle_dmg_taken,
    red_mid_dmg_taken AS mid_dmg_taken,
    red_dragon_dmg_taken AS dragon_dmg_taken,
    red_sup_dmg_taken AS sup_dmg_taken,
    red_baron_dmg_dealt AS baron_dmg_dealt,
    red_jungle_dmg_dealt AS jungle_dmg_dealt,
    red_mid_dmg_dealt AS mid_dmg_dealt,
    red_dragon_dmg_dealt AS dragon_dmg_dealt,
    red_sup_dmg_dealt AS sup_dmg_dealt,
    red_baron_total_gold AS baron_total_gold,
    red_jungle_total_gold AS jungle_total_gold,
    red_mid_total_gold AS mid_total_gold,
    red_dragon_total_gold AS dragon_total_gold,
    red_sup_total_gold AS sup_total_gold,
    red_baron_player AS baron_player,
    red_jungle_player AS jungle_player,
    red_mid_player AS mid_player,
    red_dragon_player AS dragon_player,
    red_sup_player AS sup_player
FROM map_data.maps;