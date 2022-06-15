#!/usr/bin/env bash
set -eux

docker pull asia.gcr.io/pilotstradenetwork/spyplane:latest

docker stop spyplane_flight || true && docker rm spyplane_flight || true

# If you face permissions during pull in gcloud VM, just run `docker-credential-gcr configure-docker`

cat /app/spyplane_env.list

docker run \
        -d \
        -v /spy/workspace:/app/workspace \
        --env-file /spy/env.list \
        --name spyplane_flight \
        --restart unless-stopped \
        asia.gcr.io/pilotstradenetwork/spyplane:latest

echo 'Spyplane deployment done!'
docker logs -f spyplane_flight
