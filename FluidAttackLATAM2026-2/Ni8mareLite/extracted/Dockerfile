FROM python:3.12-slim@sha256:804ddf3251a60bbf9c92e73b7566c40428d54d0e79d3428194edf40da6521286

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gosu xxd && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN useradd -m -s /bin/bash flowforge && \
    mkdir -p /app/.internal && \
    chown -R flowforge:flowforge /app

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
