#!/bin/bash

FILES=tokens/pos/cv*.txt

for f in $FILES
do
  g=$(cat $f | sed s/\,//g | sed s/\'//g | sed s/\\.//g | sed s/\"//g | sed s/\?//g | sed s/\!//g | sed s/\)//g | sed s/\(//g | sed s/\;//g | sed s/\://g | sed s/\-//g)
  echo $g >> new_pos.txt
done