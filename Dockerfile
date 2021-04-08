FROM ubuntu/ubuntu:16.04

# System maintenance
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-tk \
    graphviz \
    libxext6 \
    libxrender-dev \
    libsm6 && \
    rm -rf /var/lib/apt/lists/* && \
    /usr/bin/python3 -m pip install --upgrade pip
    
WORKDIR /notebooks

# Copy the required setup files and install the deepcell-tf dependencies
COPY README.md requirements.txt /opt/dataviz/

# Prevent reinstallation of tensorflow and install all other requirements.
RUN pip install -r /opt/dataviz/requirements.txt

# Copy over deepcell notebooks
COPY notebooks/ /notebooks/

