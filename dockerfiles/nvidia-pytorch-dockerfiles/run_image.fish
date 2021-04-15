#! /usr/bin/env fish
docker run --gpus all -p 2222:22 --name neurotic-pytorch-conda \
       --mount type=bind,source=$HOME/projects/neurotic-networks,target=/home/neurotic/neurotic-networks \
       --mount type=bind,source=/media/data,target=/home/neurotic/data \
       --mount type=bind,source=$HOME/projects/graeae,target=/home/neurotic/graeae \
       --mount type=bind,source=$HOME/projects/models/,target=/home/neurotic/models \
       -it neurotic-pytorch-conda bash
