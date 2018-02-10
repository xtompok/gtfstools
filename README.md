# gtfstools
Tools for checking and manipulating with GTFS

## Components

### `gtfs.py`
Provides simple classes to:
 * load and save GTFS files
 * load and save GTFS tables
 * export tables from database to files with applying row and table filters

### `dicttable.py`
Table with dictionary-like access to the columns, far more effective than dictionary for each row.

### gtfs-db
Tools for importing GTFS to the PostgreSQL or vice versa.

### gtfs-split
Split GTFS file geographically (very hacky and hardcoded).
