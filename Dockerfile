# Example build:
#   docker build -t mne-tools/cmb:v0.1.0 .
#
# Example usage:
#   docker run -ti -v /path/to/subjects:/workspace/subjects -v /path/to/nnUNet:/workspace/nnUNet --name CMB mne-tools/cmb:v0.1.0

# Start with NVIDIA PyTorch configured Ubuntu
FROM nvcr.io/nvidia/pytorch:24.09-py3

# Install system dependencies for FreeSurfer in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    bc binutils libgomp1 perl psmisc sudo tar tcsh unzip \
    uuid-dev vim-common libjpeg62-dev libglu1-mesa \
    libfreetype6 libxrender1 libfontconfig1 wget \
    && rm -rf /var/lib/apt/lists/*

# FreeSurfer v7.4.1 - download and install
# Users can also ADD a local tarball instead:
#   ADD freesurfer-linux-centos7_x86_64-7.4.1.tar.gz /usr/local/
RUN wget -q -O /tmp/freesurfer.tar.gz \
    https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/7.4.1/freesurfer-linux-centos7_x86_64-7.4.1.tar.gz && \
    tar -xzf /tmp/freesurfer.tar.gz -C /usr/local/ && \
    rm /tmp/freesurfer.tar.gz

# Configure FreeSurfer license (user must provide license.txt in build context)
COPY license.txt /usr/local/freesurfer/.license

# Environment variables
ENV OS=Linux
ENV FREESURFER_HOME=/usr/local/freesurfer
ENV SUBJECTS_DIR=/workspace/subjects

# nnU-Net environment
ENV nnUNet_raw_data_base=/workspace/nnUNet/nnUNet_raw
ENV nnUNet_preprocessed=/workspace/nnUNet/nnUNet_preprocessed
ENV RESULTS_FOLDER=/workspace/nnUNet/nnUNet_trained_models

# Source FreeSurfer on shell startup
RUN echo "source $FREESURFER_HOME/FreeSurferEnv.sh &>/dev/null" >> /root/.bashrc

# Create workspace directories
RUN mkdir -p /workspace/subjects /workspace/nnUNet

# Install CMB
RUN pip install --no-cache-dir cmb

WORKDIR /workspace
