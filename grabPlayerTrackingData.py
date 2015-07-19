import requests
import sys
import os
import time

season = sys.argv[1] #grab season from command line arg, a single year corresponding to the start of the season
directory = 'Data/PlayerTrackingData/' + season #set directory var

#check if directory exists for this season; if not, create it
if not os.path.exists(directory):
	os.mkdir(directory)

#set base request URL
base_url = "http://stats.nba.com/js/data/sportvu/" + season + "/"
#set extensions for each request, will also be used to open/save file
speed_data_url = "speedData.json"
touches_data_url = "touchesData.json"
passing_data_url = "passingData.json"
defense_data_url = "defenseData.json"
rebounding_data_url = "reboundingData.json"
drives_data_url = "drivesData.json"
catchShoot_data_url = "catchShootData.json"
pullUp_data_url = "pullUpShootData.json"
shooting_data_url = "shootingData.json"

#create list of all request URL's
request_urls = [speed_data_url, touches_data_url, passing_data_url, defense_data_url, rebounding_data_url, drives_data_url, catchShoot_data_url, pullUp_data_url, shooting_data_url]

#change to correct directory
os.chdir(directory)
for url_extension in request_urls:
	response = requests.get(base_url + url_extension) #get response data
	file_name = url_extension[:-5] + ".txt" #set file name
	f = open(file_name, 'w') #open file, creating it if it doesn't exist
	f.write(response.text) #write response data to file
	f.close #close file
	print "System sleeping, just retrieved " + url_extension
	time.sleep(10) #put program to sleep to avoid overloading the server
	

