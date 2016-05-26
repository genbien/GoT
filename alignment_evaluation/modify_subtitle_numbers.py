aligned_file = 'manual_alignment_subtitles_transcripts_ep01.txt'
out_file     = 'mod_manual_alignment_subtitles_transcripts_ep01.txt'

out = open(out_file, 'w')

num_pre = 0

with open(aligned_file) as f:
	for line in f:
		line = line.rstrip()
		if line.startswith('%'):
			out.write(line+'\n')
		else:
			line = line.split('\t')
			line[0] = int(line[0])
			while line[0] <= num_pre:
				line[0] = line[0] + 1
			num_pre = line[0]
			line[0] = line[0] - 1
			out.write(str(line[0])+'\t'+line[1]+'\n')

