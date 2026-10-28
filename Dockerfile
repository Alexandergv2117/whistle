# syntax=docker/dockerfile:1

# ---- Stage 1: build dependencies in an isolated virtualenv ----
FROM python:3.14-alpine AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# ---- Stage 2: minimal runtime image ----
FROM python:3.14-alpine AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

RUN addgroup -S -g 10001 whistle \
    && adduser -S -u 10001 -G whistle -H -s /sbin/nologin whistle

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY --chown=root:root --chmod=0444 app.py .

USER 10001:10001

CMD ["python", "app.py"]
