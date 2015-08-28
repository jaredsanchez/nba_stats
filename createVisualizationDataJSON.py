import os
import sys
import json


def processBasicPlayerStats(bs_obj, data, mappings, home_team_id, vis_team_id, winning_team_id, game_id, game_date, game_season):
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
		w_a = 'Win' if str(player_stats[1]) == winning_team_id else 'Loss'

		#check if player_id in data dic, if not creat dict for them
		if player_id not in data['players']: data['players'][player_id] = {}
		#check if there is a dict for this season for this player, if not, create it
		if game_season not in data['players'][player_id]: data['players'][player_id][game_season] = {}

		#create game id dict for this player in this season; set game id values and create stats dict
		stat_vals = player_stats[8:] #stats vals

		# convert minutes from a string into an integer
		if stat_vals[0] != None:
			minutes_as_list = stat_vals[0].split(':')
			stat_vals[0] = float(minutes_as_list[0] + '.' + str(int(minutes_as_list[1])/60))

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
		data['teams'][team_id][game_season][game_id] = {'date': game_date, 'opponent': opp_abbr, 'home_or_away': h_a, 'stats': stats, 'win_or_loss': w_a}



def processInactivePlayers(bs_obj, data, mappings, home_team_id, vis_team_id, winning_team_id, game_id, game_date, game_season):
	#get inactive players for game, create stat keys
	inactive_players = bs_obj['resultSets'][9]['rowSet']
	stat_keys = set(bs_obj['resultSets'][4]['headers'][8:] + bs_obj['resultSets'][11]['headers'][9:] + bs_obj['resultSets'][13]['headers'][9:])#stats keys; first=basic, second=tracking, third=advanced

	#loop through each inactive player
	for player in inactive_players:
		player_id = player[0]
		#add player to mappings if not already there
		if player_id not in mappings['players']: mappings['players'][player_id] = {'player_id': player_id, 'player_name': player[1] + ' ' + player[2]}

		#determine if player was home or away
		h_a = 'Home' if player[4] == home_team_id else 'Away' #set home or away var
		team_abbr = mappings['teams'][home_team_id]['abbr'] if player[4] == home_team_id else mappings['teams'][vis_team_id]['abbr'] #set team_abbr var
		opp_abbr = mappings['teams'][vis_team_id]['abbr'] if player[4] == home_team_id else mappings['teams'][home_team_id]['abbr'] #set team_abbr var

		#determine if player's team won the game
		w_a = 'Win' if player[4] == winning_team_id else 'Loss'

		#check if player_id in data dic, if not creat dict for them
		if player_id not in data['players']: data['players'][player_id] = {}
		#check if there is a dict for this season for this player, if not, create it
		if game_season not in data['players'][player_id]: data['players'][player_id][game_season] = {}

		#create game id dict for this player in this season; set game id values and create stats dict
		stat_vals = [None] * len(stat_keys)
		stats = dict(zip(stat_keys, stat_vals))
		data['players'][player_id][game_season][game_id] = {'date': game_date, 'team': team_abbr, 'opponent': opp_abbr, 'home_or_away': h_a, 'stats': stats, 'win_or_loss': w_a} 



def processPlayerTrackingPlayers(bs_obj, data, game_id, game_season):
	#get player tracking stats for game, create stat keys
	player_tracking_stats = bs_obj['resultSets'][11]['rowSet']
	stat_keys = bs_obj['resultSets'][11]['headers'][9:]

	#loop through each player
	for player_stats in player_tracking_stats:
		player_id = player_stats[4]

		#create game id dict for this player in this season; set game id values and create stats dict
		#account for mismatched null and 0 values for players who didnt play in game by setting player tracking vals to null to match player stats
		stat_vals = player_stats[9:] if player_stats[8] != '0:00' else [None]*20 #stats vals
		stats = dict(zip(stat_keys, stat_vals))

		#merge existing stats with player tracking stats from this function
		merged_stats = merge_two_dicts(data['players'][player_id][game_season][game_id]['stats'], stats)

		#update stats in data obj to new, merged stats
		data['players'][player_id][game_season][game_id]['stats'] = merged_stats



def processPlayerTrackingTeams(bs_obj, data, game_id, game_season):
	#get team player tracking stats for game, create stat keys
	team_player_tracking_stats = bs_obj['resultSets'][12]['rowSet']
	stat_keys = bs_obj['resultSets'][12]['headers'][6:]

	#add teams to data obj
	for team_stats in team_player_tracking_stats:
		team_id = str(team_stats[1])

		#creat dict for this game for this team in this season
		stat_vals = team_stats[6:] #stats vals
		stats = dict(zip(stat_keys, stat_vals))

		#merge existing stats with team player tracking stats from this function
		merged_stats = merge_two_dicts(data['teams'][team_id][game_season][game_id]['stats'], stats)

		#update stats in data obj to new, merged stats
		data['teams'][team_id][game_season][game_id]['stats'] = merged_stats



def processAdvancedPlayerStats(bs_obj, data, game_id, game_season):
	#get advanced player stats for game, create stat keys
	advanced_player_stats = bs_obj['resultSets'][13]['rowSet']
	stat_keys = bs_obj['resultSets'][13]['headers'][9:]

	#loop through each player
	for player_stats in advanced_player_stats:
		player_id = player_stats[4]

		#create game id dict for this player in this season; set game id values and create stats dict
		#account for mismatched null and 0 values for players who didnt play in game by setting player vals to null to match player stats
		stat_vals = player_stats[9:] if player_stats[8] != None else [None]*20 #stats vals
		stats = dict(zip(stat_keys, stat_vals))

		#merge existing stats with player tracking stats from this function
		merged_stats = merge_two_dicts(data['players'][player_id][game_season][game_id]['stats'], stats)

		#update stats in data obj to new, merged stats
		data['players'][player_id][game_season][game_id]['stats'] = merged_stats



def processAdvancedTeamStats(bs_obj, data, game_id, game_season):
	#get advanced team stats for game, create stat keys
	advanced_team_stats = bs_obj['resultSets'][14]['rowSet']
	stat_keys = bs_obj['resultSets'][14]['headers'][6:]

	#add teams to data obj
	for team_stats in advanced_team_stats:
		team_id = str(team_stats[1])

		#creat dict for this game for this team in this season
		stat_vals = team_stats[6:] #stats vals
		stats = dict(zip(stat_keys, stat_vals))

		#merge existing stats with team player tracking stats from this function
		merged_stats = merge_two_dicts(data['teams'][team_id][game_season][game_id]['stats'], stats)

		#update stats in data obj to new, merged stats
		data['teams'][team_id][game_season][game_id]['stats'] = merged_stats



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
	#create empty dict to add data to
	data = {'players': {}, 'teams': {}}

	#get mappings
	#CONDSIDER RUNNING createTeamMappings.py TO ENSURE MAPPINGS EXIST
	mappings_text = open('Data/mappings.txt').read()
	mappings_obj = json.loads(mappings_text)

	#get all box score files
	bs_files = os.listdir('Data/BoxScores/regularSeason/2014/') #CONSIDER MAKING YEAR A SYS ARG

	#loop through all box score files
	for f in bs_files: 
		#create boxscore object
		bs_text = open('Data/BoxScores/regularSeason/2014/' + f).read()
		bs_obj = json.loads(bs_text)

		#Game variables
		game_id = bs_obj['parameters']['GameID'] #set game id
		game_season = bs_obj['resultSets'][0]['rowSet'][0][8] #set the season for this game

		game_date = bs_obj['resultSets'][0]['rowSet'][0][0] #set game date
		game_date = game_date[:10] #strip time off game date, leaving just yyyy-dd-mm; CONSIDER REFORMATTING DATE

		home_team_id = str(bs_obj['resultSets'][0]['rowSet'][0][6]) #home team id
		vis_team_id = str(bs_obj['resultSets'][0]['rowSet'][0][7]) #vis team id
		winning_team_id = determineWinner(bs_obj)

		#process all the stats
		processBasicPlayerStats(bs_obj, data, mappings_obj, home_team_id, vis_team_id, winning_team_id, game_id, game_date, game_season) #basic player stats
		processBasicTeamStats(bs_obj, data, mappings_obj, home_team_id, vis_team_id, winning_team_id, game_id, game_date, game_season) #basic team stats 
		processInactivePlayers(bs_obj, data, mappings_obj, home_team_id, vis_team_id, winning_team_id, game_id, game_date, game_season) #inactive players
		#can eliminate some args because players and teams already have information about win/loss, home/away, and game_date
		processPlayerTrackingPlayers(bs_obj, data, game_id, game_season) #player track players
		processPlayerTrackingTeams(bs_obj, data, game_id, game_season) #player track team
		processAdvancedPlayerStats(bs_obj, data, game_id, game_season) #advanced player stats
		processAdvancedTeamStats(bs_obj, data, game_id, game_season) #team advanced stats

	#write data to visaulation file
	f = open('Data/visualizationData.txt', 'w') #open file, creating or overwriting it
	f.write(json.dumps(data)) #write response data to file
	f.close #close file

	#write data to mappings file
	map_file = open('Data/mappings.txt', 'w')
	map_file.write(json.dumps(mappings_obj))
	map_file.close

main()



