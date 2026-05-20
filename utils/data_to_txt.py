import os
from db.teams import Team
from db.players import Player


def write_data_to_txt(data, filename):

    filename = f"logs/{filename}.txt"

    if not os.path.exists(filename):
        with open(filename, "w") as file:
            pass  # Create an empty file if it doesn't exist

    with open(filename, "a") as file:
        file.write(f"{data}\n")


def get_teams_txt():
    for team in Team.teams:
        holder = f"""{team.tid}: {team.name} ({team.short_name})
Table:  {team.table},
Expect: {team.expected},
Streng: {team.strength},
"""
        write_data_to_txt(holder, "Teams")


def get_players_txt():
    for player in Player.players:
        holder = f"""{player.id}: {player.team_code} -> {player.web_name}
Cost:   {player.now_cost}
TPoints:{player.total_points}
Status: {player.status}
Form:   {player.form}
Element:{player.element_type}
Stats:  {player.stats}
fpl_s:  {player.fpl_stats}
Rank:   {player.rank}
Expext: {player.expected}
SP90:   {player.stats_per_90}
"""
        write_data_to_txt(holder, "Players")


def getffixture