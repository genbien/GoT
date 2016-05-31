if [ $1 != "01" -a $1 != "02" -a $1 != "03" ]
	then
		echo "Usage: sh run_eval.sh episode_number"
	else
		python srt_to_index.py $1 > good_manual_align_ep$1.txt
		cat aligned_GameOfThrones.Season01.Episode$1.txt | cut -d' ' -f3- > bad_auto_align_ep_$1.txt
		diff -y good_manual_align_ep$1.txt bad_auto_align_ep_$1.txt | grep --color  '|\|>'
		# diff -y good_manual_align_ep$1.txt bad_auto_align_ep_$1.txt
fi