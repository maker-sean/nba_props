#Import List
from datetime import datetime, timedelta
import inquirer
from pprint import pprint
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import numpy as np


#Various links to pull the necessary data, currently have to split it across 3 sites, ideally get this down to 1 current one
nba_url_v2 = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
nba_url_v3 = "https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba"
nba_url_core = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba"


def graph_assists(team_data_dict, team_name, sorted_assist_value_list, date_list, sorted_game_id_list, player_name, sorted_minutes_list, sorted_rebounds_list, sorted_points_value_list, sorted_estimatedPossessions_list):

    all_game_date_list = []
    graph_assist_list = []
    graph_rebounds_list = []
    graph_minutes_list = []
    graph_points_list = []
    graph_estimatedPossessions_list = []

    for i in team_data_dict[team_name]["games"]:
        game_date = i["date"][0:10]
        game_yyyy = int(i["date"][0:4])
        game_mm = int(i["date"][5:7])
        game_dd = int(i["date"][8:10])
        obj_game_date = datetime(game_yyyy, game_mm, game_dd)
        today_date = datetime.now().date()
        #print(game_date, today_date)
        if obj_game_date < datetime.now():
            all_game_date_list.append(game_date)
            graph_assist_list.append(0)
            graph_rebounds_list.append(0)
            graph_minutes_list.append(0)
            graph_points_list.append(0)
            graph_estimatedPossessions_list.append(0)

    list_counter = 0
    for played_game in date_list:
        if played_game in all_game_date_list:
            list_idx = all_game_date_list.index(played_game)
            graph_assist_list[list_idx] = sorted_assist_value_list[list_counter]
            graph_rebounds_list[list_idx] = sorted_rebounds_list[list_counter]
            graph_minutes_list[list_idx] = sorted_minutes_list[list_counter]
            graph_points_list[list_idx] = sorted_points_value_list[list_counter]
            graph_estimatedPossessions_list[list_idx] = sorted_estimatedPossessions_list[list_counter]
        list_counter += 1

    plt.plot(all_game_date_list, graph_assist_list, 's--', label="assists")

    #Draw best fit lines for assists
    x_list_total = []
    x_list_last_10 = []
    y_list_last_10 = []
    x_list_last_5 = []
    y_list_last_5 = []
    counter = 0

    game_list_length = len(all_game_date_list)
    for x_val in all_game_date_list:
        x_list_total.append(counter)
        if counter >= game_list_length - 10:
            if int(graph_minutes_list[counter]) > 0:
                x_list_last_10.append(counter)
                y_list_last_10.append(graph_assist_list[counter])
        if counter >= game_list_length - 5:
            if int(graph_minutes_list[counter]) > 0:
                x_list_last_5.append(counter)
                y_list_last_5.append(graph_assist_list[counter])
        counter += 1
    x = np.array(x_list_total)
    y = np.array(graph_assist_list)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x+b, '--')

    #last 10
    x = np.array(x_list_last_10)
    y = np.array(y_list_last_10)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x+b, '--')

    #last 5
    x = np.array(x_list_last_5)
    y = np.array(y_list_last_5)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x+b, '--')

    plt.plot(all_game_date_list, graph_minutes_list, 's--', label="minutes")
    plt.plot(all_game_date_list, graph_points_list, 's--', label="points")
    plt.plot(all_game_date_list, graph_estimatedPossessions_list, 's--', label="possessions")
    plt.xticks(rotation=90)
    plt.legend(loc="upper left")
    plt.title(player_name)

    plt.show()

    return

def graph_rebounds(team_data_dict, team_name, sorted_assist_value_list, date_list, sorted_game_id_list, player_name, sorted_minutes_list, sorted_rebounds_list, sorted_points_value_list, sorted_estimatedPossessions_list):

    all_game_date_list = []
    graph_assist_list = []
    graph_rebounds_list = []
    graph_minutes_list = []
    graph_points_list = []
    graph_estimatedPossessions_list = []

    for i in team_data_dict[team_name]["games"]:
        game_date = i["date"][0:10]
        game_yyyy = int(i["date"][0:4])
        game_mm = int(i["date"][5:7])
        game_dd = int(i["date"][8:10])
        obj_game_date = datetime(game_yyyy, game_mm, game_dd)
        today_date = datetime.now().date()
        #print(game_date, today_date)
        if obj_game_date < datetime.now():
            all_game_date_list.append(game_date)
            graph_assist_list.append(0)
            graph_rebounds_list.append(0)
            graph_minutes_list.append(0)
            graph_points_list.append(0)
            graph_estimatedPossessions_list.append(0)

    list_counter = 0
    for played_game in date_list:
        if played_game in all_game_date_list:
            list_idx = all_game_date_list.index(played_game)
            graph_assist_list[list_idx] = sorted_assist_value_list[list_counter]
            graph_rebounds_list[list_idx] = sorted_rebounds_list[list_counter]
            graph_minutes_list[list_idx] = sorted_minutes_list[list_counter]
            graph_points_list[list_idx] = sorted_points_value_list[list_counter]
            graph_estimatedPossessions_list[list_idx] = sorted_estimatedPossessions_list[list_counter]
        list_counter += 1

    plt.plot(all_game_date_list, graph_rebounds_list, 's--', label="rebounds")

    #Draw best fit lines for assists
    x_list_total = []
    x_list_last_10 = []
    y_list_last_10 = []
    x_list_last_5 = []
    y_list_last_5 = []
    counter = 0

    game_list_length = len(all_game_date_list)
    for x_val in all_game_date_list:
        x_list_total.append(counter)
        if counter >= game_list_length - 10:
            if int(graph_minutes_list[counter]) > 0:
                x_list_last_10.append(counter)
                y_list_last_10.append(graph_rebounds_list[counter])
        if counter >= game_list_length - 5:
            if int(graph_minutes_list[counter]) > 0:
                x_list_last_5.append(counter)
                y_list_last_5.append(graph_rebounds_list[counter])
        counter += 1
    x = np.array(x_list_total)
    y = np.array(graph_rebounds_list)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x+b, '--')

    #last 10
    x = np.array(x_list_last_10)
    y = np.array(y_list_last_10)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x+b, '--')

    #last 5
    x = np.array(x_list_last_5)
    y = np.array(y_list_last_5)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x+b, '--')


    plt.plot(all_game_date_list, graph_minutes_list, 's--', label="minutes")
    plt.plot(all_game_date_list, graph_points_list, 's--', label="points")
    plt.plot(all_game_date_list, graph_estimatedPossessions_list, 's--', label="possessions")
    plt.xticks(rotation=90)
    plt.legend(loc="upper left")
    plt.title(player_name)
    plt.show()

    return

def choose_data_type(team_data_dict, team_name, sorted_assist_value_list, date_list, sorted_game_id_list, player_name, sorted_minutes_list, sorted_rebounds_list, sorted_points_value_list, sorted_estimatedPossessions_list):

    data_type_list = ['assists', 'rebounds']

    data_type_question = [
        inquirer.List(
            "data_type",
            message="Which data statistic do you want?",
            choices=data_type_list,
        ),
    ]

    data_type_selection = inquirer.prompt(data_type_question)
    pprint(data_type_selection)

    selected_data = data_type_selection["data_type"]

    if selected_data == "assists":
        graph_assists(team_data_dict, team_name, sorted_assist_value_list, date_list, sorted_game_id_list, player_name, sorted_minutes_list, sorted_rebounds_list, sorted_points_value_list, sorted_estimatedPossessions_list)
    elif selected_data == "rebounds":
        graph_rebounds(team_data_dict, team_name, sorted_assist_value_list, date_list, sorted_game_id_list, player_name, sorted_minutes_list, sorted_rebounds_list, sorted_points_value_list, sorted_estimatedPossessions_list)

    return

def create_player_data(team_data_dict, selected_team_name, specific_player_id, team_name, player_name):

    nba_player = urlopen(nba_url_v3+"/athletes/"+specific_player_id+"/gamelog") #can add /gamelog /splits is a cool one too
    nba_player_json = json.loads(nba_player.read())

    assist_value_list = []
    date_list = []
    game_id_list = []
    minutes_list = []
    rebounds_list = []
    points_value_list = []
    estimatedPossessions_list = []

    for game_id in nba_player_json["events"].keys():
        game_player_stats = urlopen(nba_url_core+"/events/"+game_id+"/competitions/"+game_id+"/competitors/5/roster/"+specific_player_id+"/statistics/0?lang=en&region=us") #can add /gamelog /splits is a cool one too
        game_player_stats_json = json.loads(game_player_stats.read())

        game_date = nba_player_json["events"][game_id]["gameDate"]

        date_list.append(game_date[0:10])

        sorted_game_id_list = [y for _,y,_ in sorted(zip(date_list,game_id_list,assist_value_list))]

        for i in game_player_stats_json["splits"]["categories"][0]["stats"]:##seems like this can be hardcoded to be "0" and not iterate through
            if i["name"] == "minutes":
                minutes_list.append(int(i["value"]))
            if i["name"] == "rebounds":
                rebounds_list.append(int(i["value"]))
        sorted_minutes_list = [y for _,y, in sorted(zip(date_list,minutes_list))]
        sorted_rebounds_list = [y for _,y, in sorted(zip(date_list,rebounds_list))]
        for j in game_player_stats_json["splits"]["categories"][1]["stats"]:##seems like this can be hardcoded to be "0" and not iterate through
            if j["name"] == "assists":
                assist_value_list.append(int(j["value"]))
            if j["name"] == "points":
                points_value_list.append(int(j["value"]))
            if j["name"] == "estimatedPossessions":
                estimatedPossessions_list.append(int(j["value"]))
        sorted_assist_value_list = [y for _,y in sorted(zip(date_list,assist_value_list))]
        sorted_points_value_list = [y for _,y in sorted(zip(date_list,points_value_list))]
        sorted_estimatedPossessions_list = [y for _,y in sorted(zip(date_list,estimatedPossessions_list))]


    date_list.sort()

    choose_data_type(team_data_dict, selected_team_name, sorted_assist_value_list, date_list, sorted_game_id_list, player_name, sorted_minutes_list, sorted_rebounds_list,sorted_points_value_list, sorted_estimatedPossessions_list)

    return


def games_on_a_day(date):

    #pull up the specific scoreboard for the given input date
    nba_scoreboard = urlopen(nba_url_v2+"/scoreboard?dates="+date)
    nba_scoreboard_json = json.loads(nba_scoreboard.read())

    #find today's games and iterate through the games on a day
    game_id_list = []
    game_list = []

    for game_dict in nba_scoreboard_json["events"]:
        current_game_id = game_dict["id"]
        game_id_list.append(game_dict["id"])

        current_game_name = game_dict["name"]
        game_list.append(game_dict["name"])

    game_question = [
        inquirer.List(
            "selected_game",
            message="Which game do you want?",
            choices=game_list,
        ),
    ]

    game_selection = inquirer.prompt(game_question)
    pprint(game_selection)

    selected_index = game_list.index(game_selection["selected_game"])

    player_name_list = []
    player_id_list = []
    team_list_idx = []
    team_name_list = []
    team_id_list = []

    team_data_dict = {}

    game_dict = nba_scoreboard_json["events"][selected_index]

    #print(nba_scoreboard_json["events"][selected_index]["competitions"])
    for i in range(2): #0 is home team, 1 away
        team_id = game_dict["competitions"][0]["competitors"][i]["id"]
        team_name = game_dict["competitions"][0]["competitors"][i]["team"]["displayName"]

        team_data = urlopen(nba_url_v2+"/teams/"+team_id+"/roster")
        team_data_json = json.loads(team_data.read())

        season_data = urlopen(nba_url_v2+"/teams/"+team_id+"/schedule")
        season_data_json = json.loads(season_data.read())
        print(season_data_json["team"])

        team_data_dict[team_name] = {}
        team_data_dict[team_name]["id"] = team_id
        team_data_dict[team_name]["games"] = []

        i_count = 0
        for g in season_data_json["events"]:
            team_data_dict[team_name]["games"].append({})
            team_data_dict[team_name]["games"][i_count]["name"] = g["name"]
            team_data_dict[team_name]["games"][i_count]["id"] =  g["id"]
            team_data_dict[team_name]["games"][i_count]["date"] = g["date"]
            i_count += 1

        for player_info in team_data_json["athletes"]:

            team_list_idx.append(i)
            team_name_list.append(team_name)
            team_id_list.append(team_id)

            player_id_list.append(player_info["id"])
            player_name_list.append(player_info["fullName"])


    player_question = [
        inquirer.List(
            "selected_player",
            message="Which player do you want?",
            choices=player_name_list,
        ),
    ]

    player_selection = inquirer.prompt(player_question)
    pprint(player_selection)

    selected_player_index = player_name_list.index(player_selection["selected_player"])
    team_list_idx_selected = team_list_idx[selected_player_index]
    selected_team_name = team_name_list[selected_player_index]

    create_player_data(team_data_dict, selected_team_name, player_id_list[selected_player_index], team_name_list[selected_player_index], player_name_list[selected_player_index])


    return

def main():

    #Find what day the user wants games for
    day_list = ["Yesterday", "Today", "Tomorrow"]

    today = datetime.today().strftime('%Y%m%d')
    yesterday = (datetime.today() - timedelta(1)).strftime('%Y%m%d')
    tomorrow = (datetime.today() + timedelta(1)).strftime('%Y%m%d')

    actual_date_list = [yesterday, today, tomorrow]

    date_question = [
        inquirer.List(
            "selected_date",
            message="Which day of games do you want?",
            choices=day_list,
        ),
    ]

    day_selection = inquirer.prompt(date_question)
    pprint(day_selection)

    date_idx = day_list.index(day_selection["selected_date"])

    #Go ahead and find the necessary information for the dat
    games_on_a_day(actual_date_list[date_idx])

    return

if __name__ == '__main__':
    main()
