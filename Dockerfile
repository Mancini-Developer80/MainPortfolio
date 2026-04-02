FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=portfolio.settings

WORKDIR /app

# Install OS dependencies + Node.js per SCSS
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copia i file dei requisiti prima per sfruttare la cache
COPY requirements.txt package*.json ./
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install

# Copia tutto il resto
COPY . .

# Compila SCSS (genera i file in /app/css/)
RUN npm run sass:build

# Esegui collectstatic (Django prenderà i file da /app/css, /app/js, ecc. 
# e li metterà ordinatamente in /app/staticfiles/)
RUN SECRET_KEY=temp-build-key \
    DATABASE_URL=sqlite:///db.sqlite3 \
    DEBUG=False \
    python manage.py collectstatic --noinput --clear

EXPOSE 8080

CMD python manage.py migrate --noinput && \
    gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 portfolio.wsgi:application