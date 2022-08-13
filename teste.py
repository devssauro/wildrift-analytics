from shillelagh.backends.apsw.db import connect
from sqlalchemy.engine import create_engine
from sqlalchemy import inspect
import pandas as pd


# engine = create_engine(
#     "gsheets://",
#     service_account_file='wildriftanalytics-d55bf47170ff.json',
#     catalog={
#         'picks_bans': 'https://docs.google.com/spreadsheets/d/'
#                       '1i-FdBq-wx0ve85WOzVJemfQLycEs2mMuBLU82MtTn6A/edit?gid=0&headers=1',
#         'match_stats': 'https://docs.google.com/spreadsheets/d/'
#                        '1i-FdBq-wx0ve85WOzVJemfQLycEs2mMuBLU82MtTn6A/edit?gid=1509459185&headers=1',
#         'maps': 'https://docs.google.com/spreadsheets/d/'
#                 '1i-FdBq-wx0ve85WOzVJemfQLycEs2mMuBLU82MtTn6A/edit?gid=1449120246&headers=1',
#         'teams': 'https://docs.google.com/spreadsheets/d/'
#                  '1i-FdBq-wx0ve85WOzVJemfQLycEs2mMuBLU82MtTn6A/edit?gid=943800948&headers=1',
#         'players': 'https://docs.google.com/spreadsheets/d/'
#                    '1i-FdBq-wx0ve85WOzVJemfQLycEs2mMuBLU82MtTn6A/edit?gid=557693227&headers=1',
#         'champions': 'https://docs.google.com/spreadsheets/d/'
#                      '1i-FdBq-wx0ve85WOzVJemfQLycEs2mMuBLU82MtTn6A/edit?gid=1455030125&headers=1',
#     }
# )
aaa = {
  "tournament": "scrim",
  "phase": None,
  "blue_side_tag": "FLA",
  "blue_baron_player": "Disturbia",
  "blue_jungle_player": "Nagata",
  "blue_mid_player": "Elora",
  "blue_dragon_player": "Snow",
  "blue_sup_player": "Lisa",
  "red_side_tag": "SCAL",
  "red_baron_player": "Laser",
  "red_jungle_player": "Rzz",
  "red_mid_player": "7zinn",
  "red_dragon_player": "Mathsu",
  "red_sup_player": "Pilo",
  "blue_ban_1": "Olaf",
  "blue_ban_2": "Lux",
  "blue_ban_3": "Rengar",
  "blue_ban_4": "Lee Sin",
  "blue_ban_5": "Ahri",
  "blue_pick_1": "Lucian",
  "blue_pick_2": "Nami",
  "blue_pick_3": "Kha'Zix",
  "blue_pick_4": "Ziggs",
  "blue_pick_5": "Shen",
  "red_pick_1": "Camille",
  "red_pick_2": "Corki",
  "red_pick_3": "Janna",
  "red_pick_4": "Singed",
  "red_pick_5": "Jax",
  "red_ban_1": "Yuumi",
  "red_ban_2": "Senna",
  "red_ban_3": "Karma",
  "red_ban_4": "Seraphine",
  "red_ban_5": "Wukong",
  "blue_baron_pick": "Shen",
  "blue_jungle_pick": "Kha'Zix",
  "blue_mid_pick": "Ziggs",
  "blue_dragon_pick": "Lucian",
  "blue_sup_pick": "Nami",
  "red_baron_pick": "Jax",
  "red_jungle_pick": "Camille",
  "red_mid_pick": "Singed",
  "red_dragon_pick": "Corki",
  "red_sup_pick": "Janna",
  "patch": "3.3a",
  "length": "16:12",
  "length_sec": 972,
  "winner": "FLA",
  "map_number": "1",
  "blue_baron_dmg_dealt": 8952,
  "blue_jungle_dmg_dealt": 16097,
  "blue_mid_dmg_dealt": 18598,
  "blue_dragon_dmg_dealt": 17495,
  "blue_sup_dmg_dealt": 7465,
  "blue_baron_dmg_taken": 4542,
  "blue_jungle_dmg_taken": 3120,
  "blue_mid_dmg_taken": 2000,
  "blue_dragon_dmg_taken": 2743,
  "blue_sup_dmg_taken": 1806,
  "blue_baron_total_gold": 9629,
  "blue_jungle_total_gold": 13156,
  "blue_mid_total_gold": 11702,
  "blue_dragon_total_gold": 11619,
  "blue_sup_total_gold": 8447,
  "red_baron_dmg_dealt": 12763,
  "red_jungle_dmg_dealt": 13400,
  "red_mid_dmg_dealt": 10299,
  "red_dragon_dmg_dealt": 12978,
  "red_sup_dmg_dealt": 7025,
  "red_baron_dmg_taken": 8172,
  "red_jungle_dmg_taken": 7082,
  "red_mid_dmg_taken": 7817,
  "red_dragon_dmg_taken": 4296,
  "red_sup_dmg_taken": 2394,
  "red_baron_total_gold": 13013,
  "red_jungle_total_gold": 13397,
  "red_mid_total_gold": 11304,
  "red_dragon_total_gold": 13108,
  "red_sup_total_gold": 9046,
  "blue_baron_kills": 1,
  "blue_baron_deaths": 3,
  "blue_baron_assists": 7,
  "blue_jungle_kills": 5,
  "blue_jungle_deaths": 2,
  "blue_jungle_assists": 2,
  "blue_mid_kills": 0,
  "blue_mid_deaths": 3,
  "blue_mid_assists": 6,
  "blue_dragon_kills": 2,
  "blue_dragon_deaths": 4,
  "blue_dragon_assists": 2,
  "blue_sup_kills": 0,
  "blue_sup_deaths": 3,
  "blue_sup_assists": 7,
  "red_baron_kills": 4,
  "red_baron_deaths": 1,
  "red_baron_assists": 4,
  "red_jungle_kills": 6,
  "red_jungle_deaths": 1,
  "red_jungle_assists": 5,
  "red_mid_kills": 0,
  "red_mid_deaths": 1,
  "red_mid_assists": 10,
  "red_dragon_kills": 3,
  "red_dragon_deaths": 2,
  "red_dragon_assists": 8,
  "red_sup_kills": 2,
  "red_sup_deaths": 3,
  "red_sup_assists": 9,
  "winner_side": "blue",
  "blue_side_team": "Flamengo eSports",
  "red_side_team": "SCAL Esports",
}
# connection = engine.connect()
# print(f"""
#     INSERT INTO maps ({", ".join(aaa.keys())})
#     VALUES("{'", "'.join([str(aaa[c]) for c in aaa.keys()])}")
# """)
# print('", "'.join([str(aaa[c]) for c in aaa.keys()]))

# connection.execute(f"""
#     INSERT INTO maps ({", ".join(aaa.keys())})
#     VALUES("{'", "'.join([str(aaa[c]) for c in aaa.keys()])}")
# """)
# connection.close()
match_stats_columns = [
    "tournament", "team_name", "team_tag", "phase", "patch", "matchup_id",
    "map_number", "side", "length", "length_sec", "winner", "winner_side",
    "ban_1", "ban_2", "ban_3", "ban_4", "ban_5",
    "pick_1", "pick_2", "pick_3", "pick_4", "pick_5",
    "baron_pick", "jungle_pick", "mid_pick", "dragon_pick", "sup_pick",
    "baron_player", "jungle_player", "mid_player", "dragon_player", "sup_player",
    "baron_kills", "baron_deaths", "baron_assists", "baron_dmg_taken", "baron_dmg_dealt", "baron_total_gold",
    "jungle_kills", "jungle_deaths", "jungle_assists", "jungle_dmg_taken", "jungle_dmg_dealt", "jungle_total_gold",
    "mid_kills", "mid_deaths", "mid_assists", "mid_dmg_taken", "mid_dmg_dealt", "mid_total_gold",
    "dragon_kills", "dragon_deaths", "dragon_assists", "dragon_dmg_taken", "dragon_dmg_dealt", "dragon_total_gold",
    "sup_kills", "sup_deaths", "sup_assists", "sup_dmg_taken", "sup_dmg_dealt", "sup_total_gold"
]
picks_bans_columns = [
    "tournament", "matchup_id", "map_id", "map_number", "patch", "phase",
    "team_name", "team_tag", "winner", "length", "length_sec", "side",
    "position", "ban_rotation", "ban", "pick_rotation", "pick", "is_blind",
    "role", "player", "kills", "deaths", "assists", "dmg_dealt", "dmg_taken", "total_gold"
]