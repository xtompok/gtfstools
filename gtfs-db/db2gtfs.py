#!/usr/bin/python3

import psycopg2
import sys
import zipfile
import tempfile


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

tables = ["agency","stops","routes","trips","stop_times","calendar","calendar_dates"]

with zipfile.ZipFile(gtfsfile,"w",compression=zipfile.ZIP_DEFLATED) as zipf:
	for name in tables:
		print("Exporting {}...".format(name))
		tablef = tempfile.NamedTemporaryFile(mode="wb")
		copy_cmd = "COPY (SELECT * FROM {table}) TO STDOUT WITH CSV DELIMITER '{delimiter}' HEADER"
		cur.copy_expert(copy_cmd.format(table=name+"_filtered",delimiter=delimiter),tablef)
		tablef.flush()
		zipf.write(tablef.name,name+".txt")
		tablef.close()
