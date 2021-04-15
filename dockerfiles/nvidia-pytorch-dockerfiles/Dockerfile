ARG IMAGE_NAME=nvidia/cuda
FROM ${IMAGE_NAME}:11.1-devel-ubuntu20.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.5.39

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libcudnn8=$CUDNN_VERSION-1+cuda11.1 \
    libcudnn8-dev=$CUDNN_VERSION-1+cuda11.1 \
    libcusolver10 \
    rsync \
    openssh-server && \
    apt-mark hold libcudnn8 && \
    rm -rf /var/lib/apt/lists/* && \
    useradd --create-home --shell /bin/bash neurotic && \
    echo "export NLTK_DATA=/home/neurotic/data/datasets/nltk_data" >> /home/neurotic/.bashrc && \
    echo "export PATH=$PATH:/home/neurotic/.local/bin/" && \
    echo "source /opt/conda/etc/profile.d/conda.sh" >> /home/neurotic/.bashrc && \
    echo 'eval "$(register-python-argcomplete conda)"'

RUN curl https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc | gpg --dearmor > conda.gpg && \
    install -o root -g root -m 644 conda.gpg /usr/share/keyrings/conda-archive-keyring.gpg && \
    apt update && \
    apt install conda && \
    conda update conda -y && \
    conda install argcomplete -y
COPY authorized_keys /home/neurotic/.ssh/
COPY setup_conda.sh /home/neurotic/
COPY run_in_container.sh /run_in_container.sh
ENTRYPOINT service ssh restart && bash

