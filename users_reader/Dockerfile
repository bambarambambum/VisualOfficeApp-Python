# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Compilation Image
#
FROM python:3.8-slim AS compile
COPY requirements.txt .
RUN apt update && \
    apt install --no-install-recommends build-essential gcc libpq-dev -y && \
    apt clean && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Runtime Image
#
FROM python:3.8-alpine

RUN apk add --no-cache postgresql-libs
WORKDIR /reader

COPY --from=compile /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY reader.py .
CMD ["gunicorn", "-b", "0.0.0.0:8001", "reader:app"]