import os
from db.teams import Team
from db.players import Player
from db.gw_fixtures import FFixtures


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


def get_ffixture():
    for fix in FFixtures.fpl_fixtures:
        holder = f"""{fix.id}) {fix.name} - {fix.deadline_time}
{fix.is_current}, {fix.is_previous}, {fix.is_next}, {fix.finished}
Data Checked: {fix.data_checked}
Most Selected: {fix.most_selected}
Highest Score: {fix.highest_score}
Most Transferred in: {fix.most_transferred_in}
Top Element: {fix.top_element}
Most Captained: {fix.most_captained}
Most Vice Captained: {fix.most_vice_captained}
Top element info: {fix.top_element_info}
"""
        write_data_to_txt(holder, "Fpl-Fixtures")