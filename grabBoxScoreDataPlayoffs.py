import requests
import sys
import os
import time
import random

season = sys.argv[1] #grab season from command line arg, a single year corresponding to the start of the season
year = str(season[2:]) #get last two numnbers from season arg, e.g. 2014 -> '14'
base_url_front = 'http://stats.nba.com/stats/boxscoreadvanced?GameID='
base_url_back = '&RangeType=0&StartPeriod=0&EndPeriod=0&StartRange=0&EndRange=0'


#set directory var
playoff_directory = 'Data/BoxScores/playoffs/' + season + '/'

#check if directory path exists for this playoffs; if not, create it
if not os.path.exists('Data/BoxScores/playoffs/'):
	os.mkdir('Data/BoxScores/playoffs/')
if not os.path.exists(playoff_directory):
	os.mkdir(playoff_directory) 

#set front part of game id's
game_id_front = '004' + year + '00'

#set ranges for back of game id's; first # is round, second is series #, last is game #
range_first = range(101, 178) #1st round -> range is in 100's; 8 series -> 0:70; game # can be as high as 7
range_second = range(201, 238) #2nd round -> range is in 200's; 4 series -> 0:30; game # can be as high as 7
range_third = range(301, 318) #3rd round -> range is in 300's; 2 series -> 0:10; game # can be as high as 7
range_fourth = range(401, 408) #4th round -> range is in 400's; 1 series -> 0's; game # can be as high as 7


#combine all ranges
playoff_game_ids_temp = range_first + range_second + range_third + range_fourth #need temp to avoid removing consecutive items problem
playoff_game_ids = [] #will loop                                                                                                                                                           through temp list and add id's that dont end in 0, 8, or 9 to this list


#remove impossible game id's (if they end in 0, 8, or 9)
for game_id in playoff_game_ids_temp:
	# print game_id
	game_num = str(game_id)[-1]
	# print game_num
	if not (game_num == '0' or game_num == '8' or game_num == '9'):
		# print game_num
		playoff_game_ids.append(game_id)


#break into two chunks
chunk_0 = playoff_game_ids[0:55]
chunk_1 = playoff_game_ids[55:]


#make sure that you're in the right directory 
os.chdir(playoff_directory)


#make request for each playoff game
for game_id in chunk_0 + chunk_1:
	full_game_id = game_id_front + str(game_id) #prepend front of id
	response = requests.get(base_url_front + full_game_id + base_url_back) #get response data
	### ADD LOGIC TO REMOVE EMPTY GAMES ###
	### ADD LOGIC TO REMOVE EMPTY GAMES ###
	### ADD LOGIC TO REMOVE EMPTY GAMES ###
	#check that the request returned somehting in case one of the game_id's was invalid for some reason
	if response.status_code == 200:
		file_name = full_game_id + '.txt' #name file, consider changing to team names and dates
		f = open(file_name, 'w') #open file, creating or overwriting it
		f.write(response.text) #write response data to file
		f.close #close file
		print "System sleeping, just retrieved " + full_game_id + ' at ' + time.strftime("%I:%M:%S")
		time.sleep(random.randrange(7,15)) #put program to sleep for random period to avoid overloading the server and avoid detection; definitely could be shortened, but I wanted to be safe with the large number or requests being made
	else: 
		continue

print "Finised running loop"





