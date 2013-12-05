#!/bin/sh
# Call as ./gengraphs.sh ../db/github.db degree false
db=$1
datatype=$2
plot=$3
data_root=../data
db_root=../db

files=(collaborators pull followers)

for file in "${files[@]}"
do
	echo "Generating edge list for " $file
	sqlite3 $1 < $db_root/$file.sql | awk -f $data_root/transform.awk -F "|" > $data_root/$file.out
	python $datatype.py $data_root/$file.out > $data_root/$file.dat
	
	if [ $plot == "true" ]; then
		echo "Plotting";
		gnuplot -e "FILENAME='$data_root/$file.dat';TITLE='$file'" -persist $datatype.gpi;
	fi
done

