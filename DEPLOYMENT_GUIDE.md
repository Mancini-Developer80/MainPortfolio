# Deployment Checklist for Render

## Problem Solved

Your render.yaml was empty, causing Render to use default settings that didn't match your project's needs.

## What Was Done

1. **Configured render.yaml** - Properly defined the web service, database, and environment variables
2. **Created build.sh** - Build script that handles both Node.js (Sass) and Python dependencies
3. **Restored package.json** - Needed for Sass compilation during build
4. **Updated .gitignore** - Ensured css/style.css is committed (needed for deployment)

## Pre-Deployment Steps

### 1. Compile CSS Locally (One-time)

```bash
npm install
npm run sass:build
```

### 2. Verify Files Are Committed

```bash
git status
git add runtime.txt render.yaml build.sh package.json package-lock.json css/style.css
git commit -m "Configure Render deployment with proper build process"
git push
```

### 3. Environment Variables on Render Dashboard

Make sure these are set in your Render service settings:

- `SECRET_KEY` - Your Django secret key
- `DATABASE_URL` - Auto-configured by Render (from database connection)
- `CLOUDINARY_CLOUD_NAME` - Your Cloudinary cloud name
- `CLOUDINARY_API_KEY` - Your Cloudinary API key
- `CLOUDINARY_API_SECRET` - Your Cloudinary API secret

## How the Build Process Works Now

1. Render detects `runtime.txt` and uses Python 3.12.3
2. Runs `build.sh` which:
   - Installs Node.js dependencies (for Sass)
   - Compiles SCSS → CSS
   - Installs Python dependencies
   - Collects static files
   - Runs database migrations
3. Starts the app with Gunicorn

## If You Still Have Issues

### Check Build Logs

Look for these specific errors:

- Python version mismatches
- Missing dependencies
- SCSS compilation failures
- Static file collection issues

### Common Fixes

**Issue: "Python version not compatible"**

- Verify `runtime.txt` contains: `python-3.12.3`
- Check `requirements.txt` for packages that need specific Python versions

**Issue: "Module not found"**

- Ensure all packages in `requirements.txt` are compatible with Python 3.12.3
- Django 5.2.9 requires Python 3.10+, so you're fine there

**Issue: "Static files not found"**

- Make sure `css/style.css` is committed to git
- Check that `build.sh` runs successfully locally

## Alternative: Split Project (Only if needed)

If the build continues to fail, you could split into:

1. **Frontend Repository** - Just SCSS compilation, outputs to CDN
2. **Backend Repository** - Django only, pulls CSS from CDN

But with the current configuration, **this shouldn't be necessary**. The single-repo approach is simpler and Render supports it well.

## Testing Locally

Before deploying, test the build process:

```bash
# On Windows (PowerShell):
npm install
npm run sass:build
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py runserver

# Check that everything works at http://localhost:8000
```

## Next Deploy

Simply:

```bash
git add .
git commit -m "Your changes"
git push
```

Render will automatically rebuild using the new configuration.
