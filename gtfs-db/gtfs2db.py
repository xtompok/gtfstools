#!/usr/bin/python3

import psycopg2
import csv
import sys
import zipfile
import io


if len(sys.argv) < 3:
	print ("Usage: {} db gtfs".format(sys.argv[0]))
	sys.exit(1)

dbname = sys.argv[1]
gtfsfile = sys.argv[2]
if len(sys.argv) > 3:
	delimiter = sys.argv[3]
else:
	delimiter = ','

# Connect to the database
try:
        conn = psycopg2.connect('dbname='+dbname)
except:
        print("Unable to connect to database \"{}\"".format(dbname))
        sys.exit(1)
cur = conn.cursor()

with zipfile.ZipFile(gtfsfile) as gtfs:
	for fname in gtfs.namelist():
		if fname[-4:] != ".txt":
			continue
		with gtfs.open(fname) as tablefile:
			print("Copying {}".format(fname))
			tablereader = io.TextIOWrapper(tablefile,encoding='utf-8')
			reader = csv.reader(tablereader)
			header = next(reader)
			print(header)
			cur.execute("TRUNCATE TABLE {table};".format(table="gtfs_"+fname[:-4]))
			copy_cmd = "COPY {table}({columns}) FROM STDIN WITH CSV DELIMITER '{delimiter}' HEADER"
			cur.copy_expert(copy_cmd.format(table="gtfs_"+fname[:-4],columns=",".join(header),delimiter=delimiter),tablereader)
			conn.commit()


