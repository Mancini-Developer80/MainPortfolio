FROM python:3.12-slim

# Variabili d'ambiente core
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=portfolio.settings

WORKDIR /app

# Installazione dipendenze OS
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installazione Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice (Fermati qui se il .dockerignore è sbagliato)
COPY . .

# CREAZIONE FORZATA DELLE CARTELLE (Fix per STATICFILES_DIRS)
RUN mkdir -p css js img resume staticfiles static

# FIX PER django-environ
RUN touch .env

# DEBUG: Vediamo cosa vede Docker (questo apparirà nei log se fallisce)
RUN ls -la

# COLLECTSTATIC "SILENZIOSO"
RUN SECRET_KEY=build-key-123 \
    DATABASE_URL=sqlite:///db.sqlite3 \
    DEBUG=False \
    CLOUDINARY_URL=cloudinary://1:1@1 \
    python manage.py collectstatic --noinput --clear --no-post-process

EXPOSE 8080

CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "--timeout", "0", "portfolio.wsgi:application"]