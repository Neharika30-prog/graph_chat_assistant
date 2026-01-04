FROM python:3.10-slim

WORKDIR /app

# Copy shared code
COPY graph ./graph
COPY connectors ./connectors
COPY chat ./chat

# Copy api code
COPY api ./api

# Install deps
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make shared modules visible
ENV PYTHONPATH=/app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]