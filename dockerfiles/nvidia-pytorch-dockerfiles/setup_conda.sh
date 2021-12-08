#! /usr/bin/env sh

conda init
conda create --name neurotic-pytorch --clone base
echo "conda activate neurotic-pytorch" >> .bashrc
