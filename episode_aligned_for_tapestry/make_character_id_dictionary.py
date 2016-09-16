from __future__ import print_function

out_file = open('character_dictionary.py','w')

print("characters = {", file=out_file)
i = 0
with open('season1_got_list_characters.txt') as f:
	for line in f:
		line = line.rstrip()

		## compatability between online wiki list and TVD list
		if line == "Drogo":
			line = "Khal Drogo"
		if line == "Luwin":
			line = "Maester Luwin"
		if line == "Mordane":
			line = "Septa Mordane"

		## looks like: "DAENERYS_TARGARYEN": 133,
		print("\t\""+line.replace(" ", "_").upper()+"\": "+str(i)+",", file=out_file)
		i += 1
print("}", file=out_file)