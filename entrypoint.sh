#!/usr/bin/env bash
set -eux

if [[ -z "${DB_RECREATE-}" ]]; then
  echo "Not creating a new DB"
else
  echo "DB_RECREATE: ${DB_RECREATE} is defined, creating a new DB"
  rm -rf ./workspace/spyplane.db
  flyway migrate
  ./db/sqlite3 ./workspace/spyplane.db < ./db/data/spyplane_import.sql
fi

python -m spyplane.main
