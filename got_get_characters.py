from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import operator
import time
import sys
import os
import re

################################################################################
## program to get and format characters with their appearances in each of the
## episodes of season 1 of game of thrones, in order to create a narrative chart
## similar to those on xkcd (http://xkcd.com/657/)
## eventually using tapestry (https://github.com/websages/tapestry)
################################################################################

episodes = {
	'Winter is Coming (episode)': [1, []],
	'The Kingsroad': [2, []],
	'Lord Snow': [3, []],
	'Cripples, Bastards and Broken Things': [4, []],
	'The Wolf and the Lion': [5, []],
	'A Golden Crown': [6, []],
	'You Win or You Die': [7, []],
	'The Pointy End': [8, []],
	'Baelor': [9, []],
	'Fire and Blood': [10, []]
	}

## make a directory to put the character files in if it doesn't yet exist
directory = 'characters'
if not os.path.exists(directory):
	os.makedirs(directory)

char_r  = requests.get("http://gameofthrones.wikia.com/wiki/Category:Season_1_Characters?display=page&sort=alphabetical")
char_data = char_r.text
char_soup = BeautifulSoup(char_data)

char_f = open('character_page.html','w')
## save html page containing list of characters
print(char_soup.prettify().encode("utf-8"), file=char_f)

## create xml file containing all the characters (for tapestry)
characters_xml = open('characters.xml','w')
print("<characters>", file=characters_xml)

## create json file containing characters with their episodes (for tapestry)
narrative_json = open('narrative.json','w')
## why 409? (used in tapestry example)
print("{\n\t\"panels\": 409,\n\t\"scenes\": [", file=narrative_json)

char_id = 0
## for each character in season 1, match link in page of characters, go to individual character wiki link
file = "season1_got_list_characters.txt"
with open(file) as f:
	for line in f:
		line = line.rstrip()

		## fill in characters.xml
		print("\t<character group=\"0\" id=\"",char_id,"\" name=\"",line,"\" />", file=characters_xml, sep="")

		pattern = re.compile(r'\b%s\b'%line)
		## match character name in text of link to get the wiki href
		## print character name and href links in http://gameofthrones.wikia.com/
		print("> Fetching : ["+line+"] : ", char_soup.find('a', text=pattern)['href'])

		time.sleep( 5 ) ## don't make requests too quickly

		## get character's individual got wiki entry
		indiv_r  = requests.get("http://gameofthrones.wikia.com"+char_soup.find('a', text=pattern)['href'])
		indiv_data = indiv_r.text
		indiv_soup = BeautifulSoup(indiv_data)

		## save html page containing individual character
		indiv_f = open("characters/"+line+".html",'w')
		print(indiv_soup.prettify().encode("utf-8"), file=indiv_f)

		print("\tAppears in episodes :")
		## look for episode names in children of b tags (bold to indicate a characters appearance in that episode)
		for bold in indiv_soup.find_all('b'):
			try:
				children = bold.findChildren()
				for child in children:
					## print episode titles and episode numbers for each appearance
					if child['title'] in episodes:
						print("\t\t* name : \""+child['title']+"\" - number : "+str(episodes[child['title']][0]))
						episodes[child['title']][1].append(char_id)
			except KeyError:
				pass
		# break ## for debug
		char_id += 1

## print json file for tapestry
## reverse keys and values to sort by value instead of key
sorted_ep = [ (v,k) for k,v in episodes.iteritems() ]
sorted_ep.sort(reverse=False)
lines = []
for v,k in sorted_ep:
	# { "id": 1,	"name": "Winter is Coming (episode)",	"start": 10,	"duration": 30,	"chars": [..., ..., ...]},
	lines.append("\t\t{ \"id\": "+str(v[0])+",\t\"name\": \""+k+"\",\t\"start\": "+str(v[0] * 10)+",\t\"duration\": 30,\t\"chars\": "+str(v[1])+"}")
print(",\n".join(lines), file=narrative_json)

print("\t]\n}", file=narrative_json) ## end json file
print("</characters>", file=characters_xml) ## end xml file
