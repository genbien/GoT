print "characters = {"
i = 0
with open('season1_got_list_characters.txt') as f:
	for line in f:
		line = line.rstrip()
		print "\t'"+line+"': "+str(i)+","
		i += 1
print	"}"