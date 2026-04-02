FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=portfolio.settings

WORKDIR /app

# Install OS dependencies including Node.js for SCSS compilation
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies and compile SCSS
RUN npm install && npm run sass:build

# Ensure staticfiles directory exists with all compiled files
RUN mkdir -p staticfiles && \
    echo "Copying static files to staticfiles/" && \
    cp -v css/style.css staticfiles/ 2>/dev/null || echo "css/style.css not found" && \
    cp -v css/overrides.css staticfiles/ 2>/dev/null || echo "css/overrides.css not found" && \
    cp -v js/* staticfiles/ 2>/dev/null || echo "js files copy failed" && \
    cp -rv img staticfiles/ 2>/dev/null || echo "img copy failed" && \
    cp -rv resume staticfiles/ 2>/dev/null || echo "resume copy failed" && \
    echo "✓ Static files prepared"

# Run collectstatic with WhiteNoise
RUN SECRET_KEY=temp-build-key \
    DATABASE_URL=sqlite:///db.sqlite3 \
    DEBUG=False \
    CLOUDINARY_URL=cloudinary://1:1@1 \
    python manage.py collectstatic --noinput

# Verify files exist
RUN echo "Checking staticfiles/ contents:" && ls -lh staticfiles/*.css 2>/dev/null || echo "No CSS files found!"

EXPOSE 8080

CMD python manage.py migrate --noinput && \
    gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 portfolio.wsgi:application