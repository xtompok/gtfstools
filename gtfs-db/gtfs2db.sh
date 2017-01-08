#!/bin/sh

NAME=$0
DB=$1

echo "Remember to prepare schema before copying!"

TMPDIR=`mktemp -d`
unzip -o $NAME -d $TMPDIR
cd $TMPDIR

FILES="agency calendar calendar_dates routes shapes stops trips stop_times"

for f in $FILES
do
	echo "$f..."
	psql $DB -c "TRUNCATE TABLE gtfs_$f;"
	cat $f.txt | iconv -f utf-8 -t utf-8 -c |  psql $DB -c "COPY gtfs_$f FROM STDIN WITH CSV DELIMITER ',' HEADER;"
	psql $DB -c "ANALYZE gtfs_$f;"
done
cd ..
rm -rf $TMPDIR
