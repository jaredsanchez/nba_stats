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
reg_season_directory = 'Data/BoxScores/regularSeason/' + season + '/' 

#check if directory path exists for this regular season; if not, create it
if not os.path.exists('Data/BoxScores/'):
	os.mkdir('Data/BoxScores/') 
if not os.path.exists('Data/BoxScores/regularSeason/'):
	os.mkdir('Data/BoxScores/regularSeason/')
if not os.path.exists(reg_season_directory):
	os.mkdir(reg_season_directory)  

#list of game ids as int's, need to prepend '00'
reg_season_game_ids = range(21400001, 21401231)

#make sure that you're in the right directory 
os.chdir(reg_season_directory)

##### divide reg season game id's so that you can run the script in chunks instead of all at once
##### consider 2 loops, where you divide chunk and then sleep for a longer time between two loops
##### dont need to do in chunks, but it would take >7hrs all at once
##### can do multiple chunks at once if you want in for loop -> chunk_0 + chunk_1 + chunk_2
chunk_0 = reg_season_game_ids[0:60] ### COMPLETED
chunk_1 = reg_season_game_ids[60:120] ### COMPLETED
chunk_2 = reg_season_game_ids[120:180] ### COMPLETED
chunk_3 = reg_season_game_ids[180:240] ### COMPLETED
chunk_4 = reg_season_game_ids[240:300] ### COMPLETED
chunk_5 = reg_season_game_ids[300:360] ### COMPLETED
chunk_6 = reg_season_game_ids[360:420] ### COMPLETED
chunk_7 = reg_season_game_ids[420:480] ### COMPLETED
chunk_8 = reg_season_game_ids[480:540] ### COMPLETED
chunk_9 = reg_season_game_ids[540:600] ### COMPLETED
chunk_10 = reg_season_game_ids[600:660] ### COMPLETED
chunk_11 = reg_season_game_ids[660:720] ### COMPLETED
chunk_12 = reg_season_game_ids[720:780] ### COMPLETED
chunk_13 = reg_season_game_ids[780:840] ### COMPLETED
chunk_14 = reg_season_game_ids[840:900] ### COMPLETED
chunk_15 = reg_season_game_ids[900:960] ### COMPLETED
chunk_16 = reg_season_game_ids[960:1020] ### COMPLETED
chunk_17 = reg_season_game_ids[1020:1080] ### COMPLETED
chunk_18 = reg_season_game_ids[1080:1140] ### COMPLETED
chunk_19 = reg_season_game_ids[1140:1200] ### COMPLETED
chunk_20 = reg_season_game_ids[1200:1230] ### COMPLETED


# make request for each reg season gam
# each chunk should take ~22 min with good internet connection
for game_id in chunk_20:
	full_game_id = '00' + str(game_id) #prepend '00'
	response = requests.get(base_url_front + full_game_id + base_url_back) #get response data
	file_name = full_game_id + '.txt' #name file, consider changing to team names and dates
	f = open(file_name, 'w') #open file, creating or overwriting it
	f.write(response.text) #write response data to file
	f.close #close file
	print "System sleeping, just retrieved " + full_game_id + ' at ' + time.strftime("%I:%M:%S")
	time.sleep(random.randrange(7,15)) #put program to sleep for random period to avoid overloading the server and avoid detection; definitely could be shortened, but I wanted to be safe with the large number or requests being made


print "Finished pulling chunk"
























