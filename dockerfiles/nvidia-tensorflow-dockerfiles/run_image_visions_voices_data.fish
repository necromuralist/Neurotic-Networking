#! /usr/bin/env fish
docker run --gpus all -p 2222:22 --name visions-voices-data \
       --mount type=bind,source=$HOME/projects/Visions-Voices-Data,target=/home/neurotic/Visions-Voices-Data/ \
       --mount type=bind,source=/media/data,target=/home/neurotic/data \
       --mount type=bind,source=$HOME/projects/graeae,target=/home/neurotic/graeae \
       --mount type=bind,source=$HOME/projects/third-party/trax,target=/home/neurotic/trax \
       --mount type=bind,source=$HOME/projects/models/,target=/home/neurotic/models \
       -it neurotic-nvidia bash
