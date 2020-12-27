if cat /proc/version | grep microsoft; then
  DOCKER="docker.exe"
else
  DOCKER=docker
fi

set -e
REGISTRY=registry.jhalsey.com
TAG=$REGISTRY/astro-tablets:latest
GIT_HASH=$(git rev-parse --short HEAD)
$DOCKER build -t $TAG --build-arg GIT_HASH="${GIT_HASH}" .
$DOCKER login $REGISTRY
$DOCKER push $TAG
