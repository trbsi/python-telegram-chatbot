#!/usr/bin/env bash
set -e

DOCKER_CONTAINER="chatapp-django"
WORKER="chatapp-celery-worker"
BEAT="chatapp-celery-beat"

BUILD_DOCKER=false

# Parse optional flag
if [[ "$1" == "--build" ]]; then
    BUILD_DOCKER=true
fi

echo "🚀 --------------------------- Updating repository ---------------------------"
git checkout master
git checkout .
git pull --rebase

echo "🚀 --------------------------- Install dependencies ---------------------------"
docker exec -it "$DOCKER_CONTAINER" poetry install

if $BUILD_DOCKER; then
    echo "🛠️ --------------------------- Rebuilding Docker ---------------------------"
    cd docker
    docker compose up -d --build
    cd -
fi

echo "🖼️ --------------------------- Collecting static files ---------------------------"
docker exec -it "$DOCKER_CONTAINER" poetry run python manage.py collectstatic --noinput --clear

echo "📜 --------------------------- Running migrations ---------------------------"
docker exec -it "$DOCKER_CONTAINER" poetry run python manage.py migrate

echo "🔄 --------------------------- Restarting containers ---------------------------"
docker restart "$DOCKER_CONTAINER" "$WORKER" "$BEAT"

echo "✅ --------------------------- Done ---------------------------"
