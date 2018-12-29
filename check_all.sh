#!/bin/bash

RESTORE_DIR=/tmp/latest

set -e
. $HOME/.env

rm -rf $RESTORE_DIR
restic restore --path $DUMPS_DIR -t $RESTORE_DIR latest

set +e

some_failed=0

for db_name in $DB_NAMES; do
	dumpfile=`ls -lart ${RESTORE_DIR}/${DUMPS_DIR} | egrep "${db_name}-[0-9]" | tail -n 1 | awk '{print $9}'`
	$HOME/backups/check.sh $db_name ${RESTORE_DIR}/${DUMPS_DIR}/${dumpfile}
	last_status=$?
	if [ $last_status -ne 0 ]; then
		some_failed=$last_status
	fi	
done

if [ $some_failed -ne 0 ]; then
	echo "SOME CHECKS HAVE FAILED"
else
	echo "ALL GOOD!"
fi

exit $some_failed
