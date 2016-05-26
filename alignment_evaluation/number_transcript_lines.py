# program to add numbers to a transcript file for easier manual alignment

transcript_file = 'GameOfThrones.Season01.Episode01.txt'
output = 'numbered_transcripts_'+transcript_file
out = open(output, 'w')
count = 0

with open(transcript_file) as f:
	for line in f:
		out.write(str(count))
		out.write('\n')
		out.write(line)
		out.write('\n')
		count += 1