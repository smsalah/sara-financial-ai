FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including SQLite development headers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade packaging tools first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy configuration and install dependencies explicitly
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copy source code and data
COPY src/ ./src/
COPY data/ ./data/

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI server via Uvicorn
CMD ["uvicorn", "src.interfaces.api:app", "--host", "0.0.0.0", "--port", "8000"]
