if cat /proc/version | grep microsoft; then
  CMD="cmd.exe /c"
else
  CMD=
fi

set -e
REGISTRY=registry.jhalsey.com
TAG=$REGISTRY/astro-tablets:latest
$CMD docker build -t $TAG --build-arg=GIT_HASH=$(git rev-parse --short HEAD) .
$CMD docker login $REGISTRY
$CMD docker push $TAG
