#!/usr/bin/env bash
set -eux
./sqlite/sqlite3 ./workspace/spyplane.db < export.sql