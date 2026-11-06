# GPU run image for FabrykaEwolucyjna: CUDA 12.2 + Python 3.10 + PyCUDA built against it.
# Build:  docker build -t fabrykaewolucyjna-cuda:12.2 .
FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# python3-dev: PyCUDA has no Linux wheel, it is compiled here and needs Python.h
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-dev python-is-python3 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "numpy==2.2.6" "pandas==2.3.3" "pycuda==2026.1"

WORKDIR /app
