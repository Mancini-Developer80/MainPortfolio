#!/usr/bin/env python
"""
Quick test to verify Cloudinary configuration
Run this locally to check if your Cloudinary credentials work
"""
import os
import sys

print("=" * 60)
print("CLOUDINARY CONFIGURATION TEST")
print("=" * 60)

# Check if environment variables are set
cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
api_key = os.environ.get('CLOUDINARY_API_KEY')
api_secret = os.environ.get('CLOUDINARY_API_SECRET')

print("\n1. Environment Variables Check:")
print(f"   CLOUDINARY_CLOUD_NAME: {'✓ SET' if cloud_name else '✗ MISSING'}")
print(f"   CLOUDINARY_API_KEY: {'✓ SET' if api_key else '✗ MISSING'}")
print(f"   CLOUDINARY_API_SECRET: {'✓ SET' if api_secret else '✗ MISSING'}")

if not all([cloud_name, api_key, api_secret]):
    print("\n❌ ERROR: Cloudinary environment variables are NOT set!")
    print("\nYou need to:")
    print("1. Go to https://cloudinary.com/ and login")
    print("2. Get your credentials from the Dashboard")
    print("3. Set them in Render's Environment tab:")
    print("   - CLOUDINARY_CLOUD_NAME=your_cloud_name")
    print("   - CLOUDINARY_API_KEY=your_api_key")
    print("   - CLOUDINARY_API_SECRET=your_api_secret")
    sys.exit(1)

print(f"\n2. Credential Values:")
print(f"   Cloud Name: {cloud_name}")
print(f"   API Key: {api_key[:4]}...{api_key[-4:] if len(api_key) > 8 else '****'}")
print(f"   API Secret: {'*' * 20} (hidden)")

# Try to connect to Cloudinary
print("\n3. Testing Cloudinary Connection...")
try:
    import cloudinary
    import cloudinary.api
    
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )
    
    # Try to get account info
    result = cloudinary.api.ping()
    print("   ✓ Successfully connected to Cloudinary!")
    print(f"   Status: {result.get('status', 'unknown')}")
    
except ImportError:
    print("   ✗ Cloudinary package not installed")
    print("   Run: pip install cloudinary")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ Connection failed: {str(e)}")
    print("\n   Possible issues:")
    print("   - Wrong credentials")
    print("   - Network connection problem")
    print("   - Invalid API key/secret")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL CHECKS PASSED - Cloudinary is configured correctly!")
print("=" * 60)
print("\nNext steps on Render:")
print("1. Make sure these SAME variables are set in Render dashboard")
print("2. After deployment, re-upload images via admin panel")
print("3. Verify images show Cloudinary URLs (https://res.cloudinary.com/...)")
print("=" * 60)
