#!/usr/bin/env bash
set -eux
sqlite3 ./workspace/spyplane.db < export.sql
