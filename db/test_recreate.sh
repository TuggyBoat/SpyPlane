#!/usr/bin/env bash

rm -rf ./tests/test_workspace/spyplane.db
flyway -url='jdbc:sqlite:tests/test_workspace/spyplane.db' migrate
sqlite3 ./tests/test_workspace/spyplane.db < ./db/data/spyplane_import.sql
