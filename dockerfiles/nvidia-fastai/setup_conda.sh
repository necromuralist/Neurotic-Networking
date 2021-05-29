#! /usr/bin/env sh

conda create --name neurotic-fastai
conda config --add channels conda-forge
conda config --set channel_priority strict

# mamba install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -y
mamba install jupyter -y
mamba install ptpython -y
mamba install -c fastchan fastai -y
mamba install argcomplete -y

