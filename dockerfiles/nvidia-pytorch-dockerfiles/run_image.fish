#! /usr/bin/env fish

# There is currently a problem with the containers and ubuntu/debian
# see https://github.com/NVIDIA/libnvidia-container/issues/111#issuecomment-932742403
# for the comment that has the workaround
# besides adding all the devices you need to edit
# /etc/nvidia-container-runtime/config.toml

# By changing this (initially commented-out) line to true
# no-cgroups = true

# this is the last part of the error I saw (the line is really long so I'm not putting it all in):
# nvidia-container-cli: container error: cgroup subsystem devices not found: unknown.


set PROJECTS $HOME/projects
set NEUROTIC /home/neurotic

docker run --gpus all --device /dev/nvidia0 --device /dev/nvidiactl \
    --device /dev/nvidia-modeset --device /dev/nvidia-uvm \
    -p 2222:22 --name neurotic-pytorch-conda \
    --mount type=bind,source=$PROJECTS/Neurotic-Networking,target=$NEUROTIC/Neurotic-Networking \
    --mount type=bind,source=/media/data,target=$NEUROTIC/data \
    --mount type=bind,source=$PROJECTS/graeae,target=$NEUROTIC/graeae \
    --mount type=bind,source=$PROJECTS/models/,target=$NEUROTIC/models \
    -it neurotic-pytorch-conda bash
