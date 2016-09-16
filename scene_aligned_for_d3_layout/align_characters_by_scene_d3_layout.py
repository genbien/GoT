from __future__ import print_function
import collections
from character_dictionary import characters

################################################################################
##
## a python script to align characters in Game of Thrones to the scenes in
## which they appear in the interest of making a narrative chart like xkcd
##
## input : aligned subtitle-transcripts, scene segmentations
## output: data.json - a file used to make a narrative chart
## 		   (https://github.com/abcnews/d3-layout-narrative)
##
################################################################################

## pick an episode (from 01 to 10) to make a narrative file for
episode_nb = "01"

## ordered dictionary to contain all scenes (key) and lists of characters (value)
scenes = collections.OrderedDict()
scene_id = 0

## read aligned subtitle-transcripts (with timestamps and speaker information)
## file looks like:
## 3475.599 3477.333 JAIME_LANNISTER The things I do for love.
transcript_file = "../../../0_corpus/tvd/GameOfThrones/book/subtitles/GameOfThrones.Season01.Episode"+episode_nb+".txt"
with open(transcript_file) as f:
	transcripts = f.readlines()

## create json file containing characters with their scenes
narrative_json = open('data_to_append.json','w')
print("{\n\t\"characters\": [", file=narrative_json)

## fill in json for characters
## looks like:
## { "id": 69, "name": "TYRION_LANNISTER", "affiliation": "other"},
character_lines = []
for key, value in characters.iteritems():
	character_lines.append("\t\t{ \"id\": "+str(value)+", \"name\": \""+key+"\", \"affiliation\": \"other\"}")
print(",\n".join(character_lines), file=narrative_json)

print("\t],\n\t\"scenes\": [", file=narrative_json)


## scene segmentation file looks like:
## 0 10.7 beginning
## 10.7 418.7 scene_1
## 418.7 515.2 theme_song
scene_segmentation_file = "../../../0_corpus/annotations/scene_segmentation/GameOfThrones.Season01.Episode"+episode_nb+".txt"
with open(scene_segmentation_file) as f:
	for line in f:
		line = line.rstrip()
		split_seg = line.split(" ")
		scene_title = str(scene_id)+"+"+"Episode"+episode_nb+"_"+split_seg[2]
		# print("scene: "+scene_title) ## print scene title
		scenes[scene_title] = [[],[],[]]
		scenes[scene_title][0].append(split_seg[0])
		scenes[scene_title][1].append(split_seg[1])
		## go through list of transcripts for each scene
		for x in range(0,len(transcripts)):
			transcripts[x] = transcripts[x].rstrip()
			split_tr = transcripts[x].split(" ")
			## compare start-speaking time to beginning and end times of the scene
			## if speaking time falls inside the scene, print speaker
			## -- changed type to float for accurate numerical comparisons
			if float(split_tr[0]) > float(split_seg[0]) and float(split_tr[0]) < float(split_seg[1]):
				## ignore unnamed characters like MAID and GUARD
				if split_tr[2] in characters:
					# print("\tspeaker: "+split_tr[2]) ## print speakers from each scene
					## if character id not in list of characters who speak in each scene, add id to list
					if characters[split_tr[2]] not in scenes[scene_title][2]:
						scenes[scene_title][2].append(characters[split_tr[2]])
		scene_id += 1


## print json file with list of characters per scene (in chronological order)
## for each scene, looks like:
## [ "char_id", "char_id", "char_id", "char_id", "char_id" ]
lines = []
for keys,values in scenes.iteritems():
	lines.append("\t\t"+str(values[2]))
print(",\n".join(lines), file=narrative_json)

print("\t]\n}", file=narrative_json) ## end json file