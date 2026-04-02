# --- STAGE 1: Compilazione SCSS (Node.js) ---
FROM node:20-slim AS node-builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run sass:build

# --- STAGE 2: Runtime Python ---
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=portfolio.settings

WORKDIR /app

# Dipendenze OS
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installazione Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice sorgente
COPY . .

# Copia i CSS compilati dallo stage precedente
COPY --from=node-builder /app/css ./css

# Ensures staticfiles/ directory exists and has all needed files
RUN mkdir -p staticfiles && \
    cp -r css/* staticfiles/ 2>/dev/null || true && \
    cp -r js/* staticfiles/ 2>/dev/null || true && \
    cp -r img/* staticfiles/ 2>/dev/null || true && \
    cp -r resume/* staticfiles/ 2>/dev/null || true && \
    echo "✓ Static files copied to staticfiles/"

# Setup
RUN mkdir -p static

# Force collectstatic to process files with WhiteNoise
RUN SECRET_KEY=temp-build-key \
    DATABASE_URL=sqlite:///db.sqlite3 \
    DEBUG=False \
    CLOUDINARY_URL=cloudinary://1:1@1 \
    python manage.py collectstatic --noinput --clear 2>&1 | tail -5

EXPOSE 8080

# ENTRYPOINT: Run migrations then start Gunicorn
CMD python manage.py migrate --noinput && \
    gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 portfolio.wsgi:application