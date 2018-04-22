#takes a basketball dataset from kaggle and outpits specific stats of a specific player of your choice
import csv
import os

def master():
    path = os.path.join(os.path.dirname(__file__), 'basketball_master.csv')
    with open(path, 'r') as csvfile:
        master = csv.reader(csvfile, delimiter=' ', quotechar='|')
        master_list = [row[0].replace('"',"").split(",") for row in master]
        player_map = {}
        
        for player in master_list[1:]:
            if len(player) < 5:
                continue

            full_name = player[1] + ' ' + player[4]
            player_map[full_name] = player[0]
    return player_map

def get_raw_player_stats():
    path = os.path.join(os.path.dirname(__file__), 'basketball_players.csv')
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        player_list = [row[0].replace('"',"").split(",") for row in reader]
    return player_list

def get_player_stats(player_map, player_list, player_name, master_map):
    print('Year', 'PPG ', 'APG ', 'RBG ', 'MPG')
    print('--------------------------')
    
    total_points = 0
    total_assists = 0
    total_rebounds = 0
    total_minutes = 0
    years = 0

    for item in player_list:
        if item[0] == player_map[player_name]:
            points = item[master_map['points']]
            assists = item[master_map['assists']]
            
            rebounds = item[master_map['rebounds']]
            minutes = item[master_map['minutes']]
            gp = item[master_map['GP']]
            year = item[master_map['year']]

            PPG = round(int(points)/int(gp),2)
            APG = round(int(assists)/int(gp),2)
            RPG = round(int(rebounds)/int(gp),2)
            MPG = round(int(minutes)/int(gp),2)
            
            total_points += PPG
            total_assists += APG
            total_rebounds += RPG
            total_minutes += MPG
            years += 1
            
            print(year, PPG, APG, RPG, MPG)

    print('Car ', round(total_points/years, 2), round(total_assists/years, 2), round(total_rebounds/years, 2), round(total_minutes/years, 2))

def main():
    player_map = master()
    player_list = get_raw_player_stats()
    master_map = {player:player_list[0].index(player) for player in player_list[0]}
    name = input('Enter Player Name: ')
    
    get_player_stats(player_map, player_list, name, master_map)
    
if __name__ == '__main__':
    main()
