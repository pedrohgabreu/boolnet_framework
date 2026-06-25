FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    imagemagick \
    build-essential \
    flex \
    bison \
    libreadline-dev \
    libncurses5 \
    git \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/lib/x86_64-linux-gnu/libreadline.so /usr/lib/x86_64-linux-gnu/libreadline.so.6 || true

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pyboolnet maboss mpbn pandas

# Compilação nativa do núcleo em C++ do MaBoSS e envio para o PATH global do Linux
RUN git clone --depth 1 https://github.com/maboss-bkmc/MaBoSS-env-2.0.git /tmp/maboss && \
    cd /tmp/maboss/engine/src && \
    make && \
    cp MaBoSS /usr/local/bin/ && \
    rm -rf /tmp/maboss

CMD ["python", "main.py"]