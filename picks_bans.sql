SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.blue_side_tag as team_tag,
    mm.blue_side_team as team_name,
    mm.winner = mm.blue_side_tag as winner,
    mm.length as length,
    mm.length_sec as length_sec,
    mm.blue_ban_1 as ban,
    mm.blue_pick_1 as pick,
    1 as position,
    'B1' as pick_rotation,
    1 as ban_rotation,
    true as is_blind,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold
FROM map_data.maps as mm
UNION ALL
SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.blue_side_tag as team_tag,
    mm.blue_side_team as team_name,
    mm.winner = mm.blue_side_tag as winner,
    mm.length as length,
    mm.length_sec,
    mm.blue_ban_2 as ban,
    mm.blue_pick_2 as pick,
    2 as position,
    'B2/B3' as pick_rotation,
    1 as ban_rotation,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.red_baron_pick not in (mm.red_pick_1, mm.red_pick_2)
        WHEN mm.blue_jungle_pick THEN mm.red_jungle_pick not in (mm.red_pick_1, mm.red_pick_2)
        WHEN mm.blue_mid_pick THEN mm.red_mid_pick not in (mm.red_pick_1, mm.red_pick_2)
        WHEN mm.blue_dragon_pick THEN mm.red_dragon_pick not in (mm.red_pick_1, mm.red_pick_2)
        WHEN mm.blue_sup_pick THEN mm.red_sup_pick not in (mm.red_pick_1, mm.red_pick_2)
    END is_blind,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold
FROM map_data.maps as mm
UNION ALL
SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.blue_side_tag as team_tag,
    mm.blue_side_team as team_name,
    mm.winner = mm.blue_side_tag as winner,
    mm.length as length,
    mm.length_sec,
    mm.blue_ban_3 as ban,
    mm.blue_pick_3 as pick,
    3 as position,
    'B2/B3' as pick_rotation,
    1 as ban_rotation,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.red_baron_pick not in (mm.red_pick_1, mm.red_pick_2)
        WHEN mm.blue_jungle_pick THEN mm.red_jungle_pick not in (mm.red_pick_1, mm.red_pick_2)
        WHEN mm.blue_mid_pick THEN mm.red_mid_pick not in (mm.red_pick_1, mm.red_pick_2)
        WHEN mm.blue_dragon_pick THEN mm.red_dragon_pick not in (mm.red_pick_1, mm.red_pick_2)
        WHEN mm.blue_sup_pick THEN mm.red_sup_pick not in (mm.red_pick_1, mm.red_pick_2)
    END is_blind,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold
FROM map_data.maps as mm
UNION ALL
SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.blue_side_tag as team_tag,
    mm.blue_side_team as team_name,
    mm.winner = mm.blue_side_tag as winner,
    mm.length as length,
    mm.length_sec,
    mm.blue_ban_4 as ban,
    mm.blue_pick_4 as pick,
    4 as position,
    'B4/B5' as pick_rotation,
    2 as ban_rotation,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.red_baron_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
        WHEN mm.blue_jungle_pick THEN mm.red_jungle_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
        WHEN mm.blue_mid_pick THEN mm.red_mid_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
        WHEN mm.blue_dragon_pick THEN mm.red_dragon_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
        WHEN mm.blue_sup_pick THEN mm.red_sup_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
    END is_blind,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold
FROM map_data.maps as mm
UNION ALL
SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.blue_side_tag as team_tag,
    mm.blue_side_team as team_name,
    mm.winner = mm.blue_side_tag as winner,
    mm.length as length,
    mm.length_sec,
    mm.blue_ban_5 as ban,
    mm.blue_pick_5 as pick,
    5 as position,
    'B4/B5' as pick_rotation,
    2 as ban_rotation,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.red_baron_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
        WHEN mm.blue_jungle_pick THEN mm.red_jungle_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
        WHEN mm.blue_mid_pick THEN mm.red_mid_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
        WHEN mm.blue_dragon_pick THEN mm.red_dragon_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
        WHEN mm.blue_sup_pick THEN mm.red_sup_pick not in (mm.red_pick_1, mm.red_pick_2, mm.red_pick_3)
    END is_blind,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold
FROM map_data.maps as mm
UNION ALL
SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.red_side_tag as team_tag,
    mm.red_side_team as team_name,
    mm.winner = mm.red_side_tag as winner,
    mm.length as length,
    mm.length_sec,
    mm.red_ban_1 as ban,
    mm.red_pick_1 as pick,
    1 as position,
    'R1/R2' as pick_rotation,
    1 as ban_rotation,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.blue_baron_pick != mm.blue_pick_1
        WHEN mm.red_jungle_pick THEN mm.blue_jungle_pick != mm.blue_pick_1
        WHEN mm.red_mid_pick THEN mm.blue_mid_pick != mm.blue_pick_1
        WHEN mm.red_dragon_pick THEN mm.blue_dragon_pick != mm.blue_pick_1
        WHEN mm.red_sup_pick THEN mm.blue_sup_pick != mm.blue_pick_1
    END is_blind,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold
FROM map_data.maps as mm
UNION ALL
SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.red_side_tag as team_tag,
    mm.red_side_team as team_name,
    mm.winner = mm.red_side_tag as winner,
    mm.length as length,
    mm.length_sec,
    mm.red_ban_2 as ban,
    mm.red_pick_2 as pick,
    2 as position,
    'R1/R2' as pick_rotation,
    1 as ban_rotation,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.blue_baron_pick != mm.blue_pick_1
        WHEN mm.red_jungle_pick THEN mm.blue_jungle_pick != mm.blue_pick_1
        WHEN mm.red_mid_pick THEN mm.blue_mid_pick != mm.blue_pick_1
        WHEN mm.red_dragon_pick THEN mm.blue_dragon_pick != mm.blue_pick_1
        WHEN mm.red_sup_pick THEN mm.blue_sup_pick != mm.blue_pick_1
    END is_blind,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold
FROM map_data.maps as mm
UNION ALL
SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.red_side_tag as team_tag,
    mm.red_side_team as team_name,
    mm.winner = mm.red_side_tag as winner,
    mm.length as length,
    mm.length_sec,
    mm.red_ban_3 as ban,
    mm.red_pick_3 as pick,
    3 as position,
    'R3' as pick_rotation,
    1 as ban_rotation,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.blue_baron_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
        WHEN mm.red_jungle_pick THEN mm.blue_jungle_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
        WHEN mm.red_mid_pick THEN mm.blue_mid_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
        WHEN mm.red_dragon_pick THEN mm.blue_dragon_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
        WHEN mm.red_sup_pick THEN mm.blue_sup_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
    END is_blind,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold
FROM map_data.maps as mm
UNION ALL
SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.red_side_tag as team_tag,
    mm.red_side_team as team_name,
    mm.winner = mm.red_side_tag as winner,
    mm.length as length,
    mm.length_sec,
    mm.red_ban_4 as ban,
    mm.red_pick_4 as pick,
    4 as position,
    'R4' as pick_rotation,
    2 as ban_rotation,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.blue_baron_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
        WHEN mm.red_jungle_pick THEN mm.blue_jungle_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
        WHEN mm.red_mid_pick THEN mm.blue_mid_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
        WHEN mm.red_dragon_pick THEN mm.blue_dragon_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
        WHEN mm.red_sup_pick THEN mm.blue_sup_pick not in (mm.blue_pick_1, mm.blue_pick_2, mm.blue_pick_3)
    END is_blind,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold
FROM map_data.maps as mm
UNION ALL
SELECT
    GENERATE_UUID() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament as tournament,
    mm.phase as phase,
    mm.red_side_tag as team_tag,
    mm.red_side_team as team_name,
    mm.winner = mm.red_side_tag as winner,
    mm.length as length,
    mm.length_sec,
    mm.red_ban_5 as ban,
    mm.red_pick_5 as pick,
    5 as position,
    'R5' as pick_rotation,
    2 as ban_rotation,
    false as is_blind,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold
FROM map_data.maps as mm