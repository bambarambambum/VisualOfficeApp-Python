# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Compilation Image
#
FROM python:3.8-slim AS compile
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Runtime Image
#
FROM python:3.8-alpine

WORKDIR /webapp

COPY --from=compile /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY static ./static
COPY templates ./templates
COPY config webapp.py ./
CMD ["gunicorn", "-b", "0.0.0.0:8000", "webapp:app"]