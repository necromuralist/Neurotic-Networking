#! /usr/bin/env fish
docker run --gpus all -p 2222:22 --name data-neurotic \
       --mount type=bind,source=$HOME/projects/neurotic-networks,target=/home/neurotic/neurotic-networks \
       --mount type=bind,source=/media/data,target=/home/neurotic/data \
       -it neurotic-nvidia bash
