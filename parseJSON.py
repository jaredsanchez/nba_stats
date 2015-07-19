import os
import sys
import json

bs_text = open('Data/BoxScores/regularSeason/2014/0021400001.txt').read()
bs_obj = json.loads(bs_text)

data = {
	'players': {},
	'teams': {}
}

print data