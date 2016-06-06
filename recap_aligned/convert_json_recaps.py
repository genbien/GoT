################################################################################
##
## Program to convert Game of Thrones json format recaps into text format.
## Scenes are delimited with "&&&&&"
##
################################################################################

import os
import io
import json
from pprint import pprint

input_json_dir = '../../../0_corpus/recaps/recaps_json'
output_txt_dir = '../../../0_corpus/recaps/recaps_txt'

# for each json file, create a text file containing the scene recap & delimiters
for file in os.listdir(input_json_dir):
	if file.endswith('.json'):
		with open(input_json_dir+'/'+file, 'r') as f:
			json_str = f.read().replace('\n', '')

		parsed_json = json.loads(json_str)

		# change file extention to text format
		file = file.replace("json", "txt")

		with io.open(output_txt_dir+'/'+file, 'w', encoding='utf8') as out:
			for event in parsed_json["T"]["links"]:
				if 'scene' not in event:
					continue
				else:
					out.write(event['scene']+'\n')
					out.write(u'&&&&&\n')
