# from dockerhub : https://hub.docker.com/r/nvidia/cuda/#!
ARG CUDA_VERSION=12.1.0
ARG FLAVORS=devel
ARG UBUNTU=22.04

FROM nvidia/cuda:${CUDA_VERSION}-${FLAVORS}-ubuntu${UBUNTU}

# Now we'll run some stuff in the image

ARG USER_NAME=neurotic
ARG USER_HOME=/home/${USER_NAME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    openssh-server \
    rsync \
    screen && \
    rm -rf /var/lib/apt/lists/*


# Setup the user
RUN useradd --create-home --shell /bin/bash ${USER_NAME}

# setup miniconda
# mostly from https://towardsdatascience.com/conda-pip-and-docker-ftw-d64fe638dc45
# this is the miniconda version for python 3.10
# from : https://docs.conda.io/en/latest/miniconda.html#linux-installers
# retrieved: June 25, 2023
ARG MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh"
ARG SHA256SUM="aef279d6baea7f67940f16aad17ebe5f6aac97487c7c03466ff01f4819e5a651"

# # switch from root to bravo
# conda doesn't like sh, try bash
SHELL [ "/bin/bash", "--login", "-c" ]
USER ${USER_NAME}
WORKDIR ${USER_HOME}

ENV CONDA_DIR=${USER_HOME}/miniconda3

RUN --mount=type=cache,target=/root/.cache \
    wget "${MINICONDA_URL}" --output-document miniconda.sh --quiet --force-directories --directory-prefix ${CONDA_DIR} && \
    echo "${SHA256SUM} miniconda.sh" > shasum && \
    sha256sum --check --status shasum && \
    /bin/bash miniconda.sh -b -p ${CONDA_DIR} && \
    rm miniconda.sh shasum

ENV PATH=$CONDA_DIR/bin:$PATH

RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile && \
    conda init bash && \
    conda update -n base -c defaults conda

# according to https://discuss.pytorch.org/t/install-pytorch-with-cuda-12-1/174294/16
# pytorch bundles its own cuda drivers so the cuda version doesn't have to match the machine's version
# as of June 25, 2023 cuda 11.8 is their latest version
RUN --mount=type=cache,target=/root/.cache \
    conda install pytorch torchvision torchaudio pytorch-cuda=11.8 --channel pytorch --channel nvidia --yes

# I couldn't get the installation to work in any environment other than the base
# so let's go with that
RUN --mount=type=cache,target=/root/.cache \
    conda install pip jupyter pandas holoviews hvplot --channel conda-forge --yes && \
    echo "conda activate base" >> .bashrc && \
    conda clean -ayf

COPY --chown=neurotic:neurotic authorized_keys /home/neurotic/.ssh/
COPY --chown=neurotic:neurotic screenrc /home/neurotic/.screenrc

# switch back so the ENTRYPOINT works okay 
USER root
WORKDIR /
ENTRYPOINT service ssh restart && bash

