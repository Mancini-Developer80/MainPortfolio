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

# Copia il codice e i CSS compilati dallo stage precedente
COPY . .
COPY --from=node-builder /app/css ./css

# Setup ambiente
RUN mkdir -p css js img resume staticfiles static
RUN touch .env

# COLLECTSTATIC (Aggiornato: rimosso --no-post-process)
# Questo permette a WhiteNoise di generare le versioni compresse dei file
RUN SECRET_KEY=build-key-123 \
    DATABASE_URL=sqlite:///db.sqlite3 \
    DEBUG=False \
    CLOUDINARY_URL=cloudinary://1:1@1 \
    python manage.py collectstatic --noinput --clear

EXPOSE 8080

# ENTRYPOINT: Esegue migrazioni e poi avvia Gunicorn
CMD python manage.py migrate --noinput && \
    gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 portfolio.wsgi:application