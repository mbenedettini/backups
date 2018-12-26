## Backups check

### What is this?

A set of tools to check PostgreSQL dumps stored into a [repository](https://restic.net/).

Each dump to be checked needs a reference of table sizes against which the last dump will be checked. If current table
sizes are equal or greater the dump is considered to be okay.

### USAGE

Clone this repo in the home directory of some user already added to `docker` group

Requires Python >= 3.6. Also, `pip3 install psycopg2`

In the home directory, create a .env file containing the following env variables, required in order to access the restic repo: 
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `RESTIC_PASSWORD`, `RESTIC_REPOSITORY`

In $HOME/references, add a .log file for each database you want to check with the output of the following sql clause:

```
SELECT nspname || '.' || relname AS "relation",
    pg_total_relation_size(C.oid) AS "total_size"
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema')
    AND C.relkind <> 'i'
    AND nspname !~ '^pg_toast'
  ORDER BY pg_total_relation_size(C.oid) DESC
  LIMIT 20
```

The output of that command will be the reference to check table sizes so it would be a good idea to keep references up to date as much as possible.

Finally, you can give it a try:

`DUMPS_DIR="/storage/backup/dumps" DB_NAMES="tramitar" backups/check_all.sh`

where:
DUMPS_DIR contains the name of the directory where db dumps are stored in restic
DB_NAMES is a list of db names to be checked, names included here must match dumps name within DUMPS_DIR (for example `db_name-4.pg`) and also size references (for example `references/db_name.log`)
