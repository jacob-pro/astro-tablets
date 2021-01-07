if cat /proc/version | grep microsoft; then
  DOCKER="docker.exe"
  GIT="git.exe"
else
  DOCKER=docker
  GIT=git
fi

set -e

REGISTRY=registry.jhalsey.com
TAG=$REGISTRY/astro-tablets:latest

GIT_HASH=$(git rev-parse --short HEAD)
set +e
$GIT diff --exit-code --quiet
GIT_MODIFIED=$?
set -e

echo "$GIT_HASH modified = $GIT_MODIFIED"

$DOCKER build -t $TAG --build-arg GIT_HASH="${GIT_HASH}" --build-arg GIT_MODIFIED="${GIT_MODIFIED}" .
$DOCKER login $REGISTRY
$DOCKER push $TAG
