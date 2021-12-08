#! /usr/bin/env fish
set -x DOCKER_BUILDKIT 1
docker build -t neurotic-pytorch-conda .
