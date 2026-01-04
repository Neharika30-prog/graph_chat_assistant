FROM python:3.10-slim

WORKDIR /app

# Copy shared code FIRST
COPY graph ./graph
COPY connectors ./connectors
COPY chat ./chat
COPY infra ./infra

# Copy ingest code
COPY ingest ./ingest

# Install deps
COPY ingest/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "ingest/entrypoint.py"]

