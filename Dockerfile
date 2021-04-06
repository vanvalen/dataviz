# Use tensorflow/tensorflow as the base image
# Change the build arg to edit the tensorflow version.
# Only supporting python3.
ARG TF_VERSION=2.4.1-gpu

FROM tensorflow/tensorflow:${TF_VERSION}

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
RUN sed -i "/tensorflow>/d" /opt/dataviz/requirements.txt && \
    pip install -r /opt/dataviz/requirements.txt

# Copy over deepcell notebooks
COPY notebooks/ /notebooks/

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
