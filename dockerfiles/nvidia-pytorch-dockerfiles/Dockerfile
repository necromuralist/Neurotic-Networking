ARG CUDA_VERSION=11.4.2
ARG FLAVORS=cudnn8-devel
ARG DISTRIBUTION=ubuntu20.04

FROM nvidia/cuda:${CUDA_VERSION}-${FLAVORS}-${DISTRIBUTION}

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

ARG MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
ARG SHA256SUM="1ea2f885b4dbc3098662845560bc64271eb17085387a70c2ba3f29fff6f8d52f"
ARG CONDA_VERSION=py39_4.10.3

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

RUN --mount=type=cache,target=/root/.cache \
    conda install pytorch torchvision torchaudio cudatoolkit --channel pytorch --yes

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

