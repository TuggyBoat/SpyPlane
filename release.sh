#!/usr/bin/env bash

poetry export --without-hashes -f requirements.txt  > generated_requirements.txt
docker build . -t asia.gcr.io/pilotstradenetwork/spyplane:latest
docker push asia.gcr.io/pilotstradenetwork/spyplane:latest
