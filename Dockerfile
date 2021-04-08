FROM ubuntu:20.04

# System maintenance
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common && \
    apt-add-repository universe

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    software-properties-common \
    python3-tk \
    graphviz \
    libxext6 \
    libxrender-dev \
    libsm6 \ 
    python3-pip && \
    rm -rf /var/lib/apt/lists/*
    
WORKDIR /notebooks

# Copy the required setup files and install the deepcell-tf dependencies
COPY README.md requirements.txt /opt/dataviz/

# Prevent reinstallation of tensorflow and install all other requirements.
RUN pip3 install -r /opt/dataviz/requirements.txt

# Copy over deepcell notebooks
COPY notebooks/ /notebooks/

