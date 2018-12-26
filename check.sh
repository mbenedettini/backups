#!/bin/bash
set -e
. $HOME/.env

db_name=$1
dump_file=$2

echo "Restoring db $db_name from file $dump_file"

docker run --name restore -p 5433:5432 -e POSTGRES_PASSWORD="" -e POSTGRES_USER=restore -d postgres:9.5

sleep 15

pg_restore -U restore -h 127.0.0.1 -p 5433 -d restore -O -x -Fc ${dump_file}

sleep 5

set +e

python3.6 $HOME/backups/check.py $HOME/references/${db_name}.log
db_check_status=$?

docker kill restore
docker rm restore

exit $db_check_status
