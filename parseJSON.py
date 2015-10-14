import os
import sys
import json

'''
This is a script I wrote for a project I have been working on to gather and visualize NBA statistics. 
This code opens up all the files in a directory related to given season, all of which are gathered in a different script and stored in JSON format as .txt files.
Each file contains the information for a single game's statistics from that season.
All those box scores are then reformatted and combined into a new JSON and saved in a new .txt file (visualizationData.txt)
This new JSON formatted text file is then used later for a visualization of these NBA statistics. 
The code also extends another JSON file (mappings.txt) while generating visualizationData.txt. This file is simply used as a dictionary to lookup player and team information later. 
You can try out the project as it currently is at http://jaredsanchez.github.io/bballStats/layouts/index.html. You can also see all the code at https://github.com/jaredsanchez/nba_stats.
I plan to continue adding data as well as features to the project. 
'''


def processBasicPlayersStats(bs_obj, data, mappings, home_team_id, vis_team_id, winning_team_id, game_id, game_date, game_season):
	#basic players stats
	basic_players_stats = bs_obj['resultSets'][4]['rowSet']
	stat_keys = bs_obj['resultSets'][4]['headers'][8:] #stats keys

	#loop through each player
	for player_stats in basic_players_stats:
		player_id = player_stats[4]
		#add player to mappings if not already there
		if player_id not in mappings['players']: mappings['players'][player_id] = {'player_id': player_id, 'player_name': player_stats[5]}

		#determine if player was home or away
		h_a = 'Home' if player_stats[1] == home_team_id else 'Away' #set home or away var
		team_abbr = mappings['teams'][home_team_id]['abbr'] if player_stats[1] == home_team_id else mappings['teams'][vis_team_id]['abbr'] #set team_abbr var
		opp_abbr = mappings['teams'][vis_team_id]['abbr'] if player_stats[1] == home_team_id else mappings['teams'][home_team_id]['abbr'] #set team_abbr var

		#determine if player's team won the game
		w_a = 'Win' if player_stats[1] == winning_team_id else 'Loss'

		#check if player_id in data dic, if not creat dict for them
		if player_id not in data['players']: data['players'][player_id] = {}
		#check if there is a dict for this season for this player, if not, create it
		if game_season not in data['players'][player_id]: data['players'][player_id][game_season] = {}

		#create game id dict for this player in this season; set game id values and create stats dict
		stat_vals = player_stats[8:] #stats vals
		stats = dict(zip(stat_keys, stat_vals))
		data['players'][player_id][game_season][game_id] = {'date': game_date, 'team': team_abbr, 'opponent': opp_abbr, 'home_or_away': h_a, 'stats': stats, 'win_or_loss': w_a} 


def processBasicTeamStats(bs_obj, data, mappings, home_team_id, vis_team_id, winning_team_id, game_id, game_date, game_season):
	#make sure teams exist in data dict, if not create dict for them
	if home_team_id not in data['teams']: data['teams'][home_team_id] = {}
	if vis_team_id not in data['teams']: data['teams'][vis_team_id] = {}
	#make sure dict for this season exists for both these teams
	if game_season not in data['teams'][home_team_id]: data['teams'][home_team_id][game_season] = {}
	if game_season not in data['teams'][vis_team_id]: data['teams'][vis_team_id][game_season] = {}

	#basic team stats
	basic_teams_stats = bs_obj['resultSets'][5]['rowSet']
	stat_keys = bs_obj['resultSets'][5]['headers'][5:]

	#add teams to data obj
	for team_stats in basic_teams_stats:
		team_id = str(team_stats[1])

		#determine home or away
		h_a = 'Home' if team_id == home_team_id else 'Away'
		opp_abbr = mappings['teams'][vis_team_id]['abbr'] if h_a == 'Home' else mappings['teams'][home_team_id]['abbr']

		#determine if team won the game
		w_a = 'Win' if team_id == winning_team_id else 'Loss'

		#creat dict for this game for this team in this season
		stat_vals = team_stats[5:] #stats vals
		stats = dict(zip(stat_keys, stat_vals))
		data['teams'][team_id][game_season][game_id] = {'data': game_date, 'opponent': opp_abbr, 'home_or_away': h_a, 'stats': stats, 'win_or_loss': w_a}


#function that returns winning team id
def determineWinner(bs_obj):
	score1 = bs_obj['resultSets'][1]['rowSet'][0][-1] #first team's score
	score2 = bs_obj['resultSets'][1]['rowSet'][1][-1] #second team's score
	winner = bs_obj['resultSets'][1]['rowSet'][0][3] if score1 > score2 else bs_obj['resultSets'][1]['rowSet'][1][3] #set winner to winning team's id
	return str(winner)

def merge_two_dicts(x, y):
    #Given two dicts, merge them into a new dict as a shallow copy
    z = x.copy()
    z.update(y)
    return z

def main():
	season = sys.argv[1] #grab season from command line arg, a single year corresponding to the start of the season

	#create empty dict to add data to
	data = {'players': {}, 'teams': {}}

	#get mappings
	#CONDSIDER RUNNING createTeamMappings.py TO ENSURE MAPPINGS EXIST
	mappings_text = open('Data/mappings.txt').read()
	mappings_obj = json.loads(mappings_text)

	#get all box score files
	bs_files = os.listdir('Data/BoxScores/regularSeason/' + season + '/')

	#loop through all box score files
	for f in bs_files: 
		#create boxscore object
		bs_text = open('Data/BoxScores/regularSeason/' + season + '/' + f).read()
		bs_obj = json.loads(bs_text)

		#Game variables
		game_id = bs_obj['parameters']['GameID'] #set game id
		game_season = bs_obj['resultSets'][0]['rowSet'][0][8] #set the season for this game

		game_date = bs_obj['resultSets'][0]['rowSet'][0][0] #set game date
		game_date = game_date[:10] #strip time off game date, leaving just yyyy-dd-mm; CONSIDER REFORMATTING DATE

		home_team_id = str(bs_obj['resultSets'][0]['rowSet'][0][6]) #home team id
		vis_team_id = str(bs_obj['resultSets'][0]['rowSet'][0][7]) #vis team id
		winning_team_id = determineWinner(bs_obj)

		#basic player stats
		processBasicPlayersStats(bs_obj, data, mappings_obj, home_team_id, vis_team_id, winning_team_id, game_id, game_date, game_season)
		#basic team stats 
		processBasicTeamStats(bs_obj, data, mappings_obj, home_team_id, vis_team_id, winning_team_id, game_id, game_date, game_season)

	#write data to file
	f = open('Data/visualizationData.txt', 'w') #open file, creating or overwriting it
	f.write(json.dumps(data)) #write response data to file
	f.close #close file

	print len(data['players'])

main()



