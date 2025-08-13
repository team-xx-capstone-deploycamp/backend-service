FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Optional build tools in case wheels aren't available for your platform;
# comment these lines if you want the absolute slimmest image and your deps install fine without them.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy only the app dir (compose will mount it for dev)
COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
