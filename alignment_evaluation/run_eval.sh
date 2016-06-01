################################################################################
##
## launcher for comparison evaluation of automatic vs manual alignment of
## subtitles and transcripts.
## usage: sh run_eval.sh (01|02|03|04|05|06|07|08|09|10)
##
################################################################################

if [ $1 != "01" -a $1 != "02" -a $1 != "03" ]
	then
		echo "Usage: sh run_eval.sh episode_number"
	else
		python srt_to_index.py $1 > good/good_manual_align_ep$1.txt
		# cut off timestamps (not compared)
		cat auto_aligned/aligned_GameOfThrones.Season01.Episode$1.txt | cut -d' ' -f3- > bad/bad_auto_align_ep_$1.txt
		diff -y good/good_manual_align_ep$1.txt bad/bad_auto_align_ep_$1.txt | grep --color  '|\|>'
		## comment above line and uncomment below for basic diff (all lines)
		# diff -y good_manual_align_ep$1.txt bad_auto_align_ep_$1.txt
fi