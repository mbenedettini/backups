#!/bin/bash
DIR=/storage/backup/dumps
source /storage/backup/.env

docker exec -u postgres $(docker ps | grep irt-extranet_db | cut -f 1 -d " ") pg_dump -Fc extranet > "$DIR/extranet-$(date "+%u").pg"
docker exec -u postgres $(docker ps | grep irt-gestionlaboral_db | cut -f 1 -d " ") pg_dump -Fc gestionlaboral > "$DIR/gestionlaboral-$(date "+%u").pg"
docker exec -u postgres $(docker ps | grep irt-visitas_db | cut -f 1 -d " ") pg_dump -Fc visitas > "$DIR/irt-visitas-$(date "+%u").pg"
docker exec -u postgres $(docker ps | grep tramitar_db | cut -f 1 -d " ") pg_dump -Fc -U tramitar tramitar > "$DIR/tramitar-$(date "+%u").pg"

tar cfj $DIR/irt-www.tar.bz2 /storage/irt-www
tar cfj $DIR/traefik.tar.bz2 /storage/traefik

ls -lh $DIR | sed -re 's/^[^ ]* //'

/usr/local/bin/restic backup $DIR
/usr/local/bin/restic backup /storage/irt-extranet/storage/reports

/usr/local/bin/restic forget --keep-daily 28 --keep-weekly 8 --group-by paths --prune
