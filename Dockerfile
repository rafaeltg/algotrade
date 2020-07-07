FROM python:3.8-slim

USER root

ENV PYTHONPATH /work/algotrade:$PYTHONPATH
ENV DEBIAN_FRONTEND=noninteractive
ENV TF_XLA_FLAGS "--tf_xla_cpu_global_jit"

ADD . /work/algotrade
WORKDIR /work/algotrade

RUN apt-get update && \
    bash install_ta-lib.sh && \
    bash install_pydl.sh && \
    pip3 install --no-cache-dir -r requirements.txt -U && \
    apt-get clean && \
    apt-get autoclean -y && \
    apt-get autoremove -y && \
    rm -rf install_ta-lib.sh install_pydl.sh /var/lib/apt/lists/*

