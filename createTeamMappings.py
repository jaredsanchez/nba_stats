import json
import os


#function to create mappings
def addMappings(mappings_obj, boxScore_obj):
	#map teams
	team_id_1 = boxScore_obj['resultSets'][5]['rowSet'][0][1] #home team id
	team_id_2 = boxScore_obj['resultSets'][5]['rowSet'][1][1] #vis team id
	if not team_id_1 in mappings_obj['teams']:
		team_name = boxScore_obj['resultSets'][5]['rowSet'][0][2]
		team_city = boxScore_obj['resultSets'][5]['rowSet'][0][4]
		team_abbr = boxScore_obj['resultSets'][5]['rowSet'][0][3]
		mappings_obj['teams'][team_id_1] = {'team_id':team_id_1, 'team_name': team_name, 'team_city': team_city, 'abbr': team_abbr}
	if not team_id_2 in mappings_obj['teams']:
		team_name = boxScore_obj['resultSets'][5]['rowSet'][1][2]
		team_city = boxScore_obj['resultSets'][5]['rowSet'][1][4]
		team_abbr = boxScore_obj['resultSets'][5]['rowSet'][1][3]
		mappings_obj['teams'][team_id_2] = {'team_id':team_id_2, 'team_name': team_name, 'team_city': team_city, 'abbr': team_abbr}



#function to ensure file exists
def main():
	#list of game ids as int's, need to prepend '00'
	reg_season_game_ids = range(21400001, 21401231)

	#create mappings object
	mappings_obj = {'players': {}, 'teams':{}}

	#open files for first 20 games and create player/team mappings
	for game_id in reg_season_game_ids[:20]:
		file_name = '00' + str(game_id) + '.txt'
		bs_text = open('Data/BoxScores/regularSeason/2014/' + file_name).read()
		bs_obj = json.loads(bs_text)
		addMappings(mappings_obj, bs_obj)

	#open mappings file, creating or overwriting it
	f = open('Data/mappings.txt', 'w')

	f.write(json.dumps(mappings_obj)) #write response data to file
	f.close #close file


main()