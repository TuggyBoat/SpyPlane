#!/usr/bin/env bash

poetry export --without-hashes -f requirements.txt  > generated_requirements.txt
docker build . -t asia.gcr.io/pilotstradenetwork/spyplane:latest

docker stop spyplane_flight || true && docker rm spyplane_flight || true

# If you face permissions during pull in gcloud VM, just run `docker-credential-gcr configure-docker`

cat .env

docker run \
#        -it \
        -d \
        --env-file .env \
        --name spyplane_flight \
        --restart unless-stopped \
#        --entrypoint /bin/bash \
        asia.gcr.io/pilotstradenetwork/spyplane:latest

echo 'Spyplane deployment done!'
docker logs -f spyplane_flight
