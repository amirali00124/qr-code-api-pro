# Render Deployment Fix Guide

If you encounter the "__version__" KeyError during Render deployment, follow these steps:

## Problem
Render is trying to use Python 3.13 which may have compatibility issues with some packages.

## Solution

### Step 1: Check Python Version
Make sure your `runtime.txt` file contains:
```
python-3.11.7
```

### Step 2: Update Requirements (Already Fixed)
The `requirements.txt` now uses version ranges instead of exact versions:
```
Flask>=2.3.0,<4.0.0
Flask-CORS>=3.0.0,<5.0.0
qrcode[pil]>=7.0.0,<8.0.0
Pillow>=9.0.0,<11.0.0
reportlab>=3.6.0,<5.0.0
gunicorn>=20.0.0,<22.0.0
requests>=2.25.0,<3.0.0
```

### Step 3: Deploy Settings in Render
1. **Build Command**: `pip install -r requirements.txt`
2. **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 0 main:app`
3. **Python Version**: Auto-detect (will use runtime.txt)

### Step 4: Environment Variables
Set these in Render dashboard:
- `SESSION_SECRET`: Auto-generate a random string
- `RENDER`: Set to `true` (enables keep-alive)

### Alternative Solution (if still failing)
If the deployment still fails, try this minimal requirements.txt:
```
Flask==2.3.3
Flask-CORS==4.0.0
qrcode==7.4.2
Pillow==10.0.1
reportlab==4.0.4
gunicorn==21.2.0
requests==2.31.0
```

## Testing Deployment
1. After successful deployment, check these endpoints:
   - `GET /health` - Should return health status
   - `GET /` - Demo interface
   - `POST /api/v1/qr/url` - QR generation

## Keep-Alive Verification
Look for these logs in Render console after 2 minutes:
```
Keep-alive service started successfully
Keep-alive ping successful: 200
```

If you see these logs, the keep-alive is working and your app won't sleep!