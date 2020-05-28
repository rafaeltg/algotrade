FROM python:3.8-slim AS pydl-builder

ENV DEBIAN_FRONTEND=noninteractive
ENV TF_XLA_FLAGS "--tf_xla_cpu_global_jit"

RUN apt-get update && \
    apt-get install git -y && \
    git clone https://github.com/rafaeltg/pydl.git && \
    cd pydl && \
    pip install pip -U && \
    pip3 install --no-cache-dir -r requirements.txt -U && \
    pip3 install --no-cache-dir tensorflow && \
    python3 setup.py install -O2 && \
    cd .. && \
    rm -rf pydl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


FROM pydl-builder as builder

ENV PYTHONPATH /work/:$PYTHONPATH

ADD . /work/algotrade
WORKDIR /work/algotrade

RUN pip3 install --no-cache-dir -r requirements.txt -U
