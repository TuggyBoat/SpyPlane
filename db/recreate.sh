#!/usr/bin/env bash

rm -rf ./workspace/spyplane.db
flyway migrate
sqlite3 ./workspace/spyplane.db < ./db/data/spyplane_import.sql
