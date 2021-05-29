#! /usr/bin/env sh

conda create --name neurotic-pytorch jupyter
conda config --add channels conda-forge
conda config --set channel_priority strict
mamba install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c conda-forge -y
# conda install argcomplete -y
