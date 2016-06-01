file = 'manual_alignment_subtitles_transcripts_ep03.txt'

existing_lines = []
all_lines = []
number_of_transcripts = 348

for x in range(number_of_transcripts + 1):
	all_lines.append(str(x))

with open(file) as f:
	for line in f:
		line = line.rstrip()
		if line.startswith('%'):
			continue
		else:
			line = line.split('\t')
			existing_lines.append(line[1])

print list(set(all_lines) - set(existing_lines))
