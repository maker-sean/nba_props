#Import List
from datetime import datetime, timedelta
import json
import os
from urllib.request import urlopen

#Various links to pull the necessary data, currently have to split it across 3 sites, ideally get this down to 1 current one
nba_url_v2 = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
nba_url_v3 = "https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba"
nba_url_core = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba"

def find_games(output_dict, date):

    #pull up the specific scoreboard for the day
    nba_scoreboard = urlopen(nba_url_v2+"/scoreboard?dates="+date)
    nba_scoreboard_json = json.loads(nba_scoreboard.read())

    print(date)

    team_options_list = ["home", "away"]

    game_count = 0
    for game_dict in nba_scoreboard_json["events"]:
        current_game_id = game_dict["id"]
        current_game_name = game_dict["name"]

        output_dict["games_list"].append({})
        output_dict["games_list"][game_count]["game_id"] = current_game_id
        output_dict["games_list"][game_count]["game_name"] = current_game_name

        game_dict = nba_scoreboard_json["events"][game_count]

        for i in range(len(team_options_list)):

            team_id = game_dict["competitions"][0]["competitors"][i]["id"]
            team_name = game_dict["competitions"][0]["competitors"][i]["team"]["displayName"]

            output_dict["games_list"][game_count][team_options_list[i]] = {}
            output_dict["games_list"][game_count][team_options_list[i]]["team_id"] = team_id
            output_dict["games_list"][game_count][team_options_list[i]]["team_name"] = team_name

            team_data = urlopen(nba_url_v2+"/teams/"+team_id+"/roster")
            team_data_json = json.loads(team_data.read())

            season_data = urlopen(nba_url_v2+"/teams/"+team_id+"/schedule")
            season_data_json = json.loads(season_data.read())

            output_dict["games_list"][game_count][team_options_list[i]]["season_games"] = {}

            for g in season_data_json["events"]:

                #need to fix the day because it will be off sometimes based on the time of the game end
                game_time = g["date"][11:13]
                if int(game_time) == 0:
                    date_day = str(int(float(g["date"][8:10])-1))
                    if len(date_day) < 2:
                        date_day = "0" + date_day
                else:
                    date_day = g["date"][8:10]

                game_date = g["date"][0:4] + g["date"][5:7] + date_day
                game_name = g["name"]

                output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date] =  {}

                #output the games and classify by date, may want to classify by opponent for easier searching for comparison against certain competitors
                output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["game_name"] = g["name"]
                output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["game_id"] = g["id"]
                output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["game_date"] = g["date"]
                output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["game_statistics"] = {}

                team_list = []

                #get the list of the two teams to allow filtering later
                for z in g["competitions"][0]["competitors"]:
                    z_team = z["team"]["displayName"]
                    team_list.append(z_team)
                    if z_team == team_name:
                        output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["homeAway"] = z["homeAway"]

                #for each game find statistics, unclear how to look up the scoreboard of a particular game without just filtering by the date

                game_scoreboard = urlopen(nba_url_v2+"/scoreboard?dates="+game_date)
                game_scoreboard_json = json.loads(game_scoreboard.read())

                for found_game in game_scoreboard_json["events"]:
                    #print(found_game["competitions"][0]["competitors"][0]["team"]["displayName"])
                    #print(team_name)

                    #print(found_game["competitions"][0]["attendance"]

                    if found_game["name"] == game_name:
                        output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["game_statistics"]["attendance"] = found_game["competitions"][0]["attendance"]
                        for twoteams in found_game["competitions"][0]["competitors"]:
                            if twoteams["homeAway"] == "home":
                                output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["game_statistics"]["homeTeam"] = twoteams["team"]["displayName"]
                                location_key = "home_team_stats"
                                homeAway_idx = 0
                            elif twoteams["homeAway"] == "away":
                                output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["game_statistics"]["awayTeam"] = twoteams["team"]["displayName"]
                                location_key = "away_team_stats"
                                homeAway_idx = 1
                            output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["game_statistics"][location_key] = {}
                            #print(twoteams["team"]["displayName"])
                            if twoteams["team"]["displayName"] in team_list:
                                #print("yep!")
                                for stat_dictionary in twoteams["statistics"]:
                                    output_dict["games_list"][game_count][team_options_list[i]]["season_games"][game_date]["game_statistics"][location_key][stat_dictionary["name"]] = float(stat_dictionary["displayValue"])
        game_count += 1


    return output_dict

def create_output_dict(today):

    output_dict = {}

    output_dict["global_information"] = {}
    output_dict["global_information"]["date"] = today

    output_dict["games_list"] = []

    return output_dict

def main():

    #Find the game stats for the day
    today = datetime.today().strftime('%Y%m%d')

    output_dict = create_output_dict(today)

    output_directory_name = "game_data"
    cwd = os.getcwd()
    output_directory_path = cwd + "/game_data/"

    output_dict = find_games(output_dict, today)

    with open(output_directory_path +  "game_data_" + today + ".json", 'w') as fh:
        fh.write(json.dumps(output_dict, indent=2))

    return

if __name__ == '__main__':
    main()
