#! /usr/bin/env sh
# installing software-properties-common gives the command to add
# a ppa, but the installation is interactive and breaks the image creation
# so do this stuff afterwards
apt update
apt install -y --no-install-recommends software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y --no-install-recommends \
    python3.9 \
    python3.9-dev \
    python3.9-distutils \
    python3-pip \

pip3 install --upgrade jax jaxlib==0.1.57+cuda111 -f https://storage.googleapis.com/jax-releases/jax_releases.html    
pip3 install jupyter tensorflow matplotlib
ln -s /usr/bin/python3 /usr/bin/python
ln -s /usr/bin/pip3 /usr/bin/pip


