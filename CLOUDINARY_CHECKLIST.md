# Cloudinary Configuration Checklist

## ✅ Fixed Issues (Just Deployed)

1. Removed duplicate `DEFAULT_FILE_STORAGE` declaration in settings.py
2. Fixed template syntax in `_project_card.html` (changed from `{% static %}` to `.url`)
3. Cloudinary storage is now properly configured

## 🔍 Required: Verify Render Environment Variables

**CRITICAL:** Go to your Render dashboard and verify these environment variables are set:

### Required Cloudinary Variables:

1. **CLOUDINARY_CLOUD_NAME** = `your-cloud-name`
2. **CLOUDINARY_API_KEY** = `your-api-key`
3. **CLOUDINARY_API_SECRET** = `your-api-secret`

### How to Check:

1. Go to https://dashboard.render.com/
2. Click on your `portfolio-j2jx` service
3. Go to **Environment** tab
4. Verify all three Cloudinary variables are present and have values

### Where to Get These Values:

1. Go to https://cloudinary.com/
2. Login to your account
3. Go to **Dashboard**
4. You'll see:
   - **Cloud Name** (e.g., `dmxxxxxxxxx`)
   - **API Key** (e.g., `123456789012345`)
   - **API Secret** (click "Reveal" to see it)

## 📋 After Deployment Completes (5-10 minutes)

### Step 1: Verify Deployment

- Check Render dashboard for deployment status
- Look for "Live" status with green checkmark

### Step 2: Clear Old Images from Database

For each case study in the admin panel:

1. Go to https://giuseppemancini.dev/admin/pages/casestudy/
2. Click on a case study
3. Scroll to the Image field
4. **Check the "Clear" checkbox** to remove old image reference
5. Click "Save"
6. Edit the same case study again
7. **Upload the image again** from your local `media/case_studies/` folder
8. Click "Save"

### Step 3: Verify Cloudinary Upload

After uploading an image, check the image field in the admin:

- ❌ **Wrong**: `case_studies/myflix.png` (local path - will cause 404)
- ✅ **Correct**: `https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/case_studies/myflix.png`

If you see a Cloudinary URL, the upload worked!

### Step 4: Test on Frontend

- Visit https://giuseppemancini.dev/
- Check if images load correctly (no 404 errors in console)
- Test different pages: home, projects, case study details

## 🐛 Still Getting 404 Errors?

### Check Browser Console:

- Right-click → Inspect → Console tab
- Look at the image URL in the error
- If it says `media/case_studies/...` instead of `https://res.cloudinary.com/...`, the image wasn't uploaded to Cloudinary

### Common Issues:

1. **Environment variables not set on Render** → Check Render dashboard
2. **Old images still in database** → Re-upload images after deployment completes
3. **Browser cache** → Hard refresh with Ctrl+F5
4. **Deployment not complete** → Wait for "Live" status on Render

## ✅ Success Indicators

- ✓ No 404 errors in browser console
- ✓ Images display correctly on all pages
- ✓ Admin panel shows Cloudinary URLs for images
- ✓ Images persist across deployments

## 📞 Need Help?

If you've followed all steps and still see 404 errors:

1. Copy the exact 404 URL from browser console
2. Copy the image field value from Django admin
3. Screenshot of Render environment variables (blur the secret values)
