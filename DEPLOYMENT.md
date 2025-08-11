# Deployment Guide - GitHub + Render

This guide explains how to deploy your QR Code Generator API to Render using GitHub for free, including the keep-alive functionality to prevent sleeping.

## Prerequisites

1. GitHub account
2. Render account (free tier)
3. Your QR Code API project code

## Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your local code to the repository:

```bash
git init
git add .
git commit -m "Initial commit - QR Code API with keep-alive"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

## Step 2: Deploy on Render

1. Go to [Render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the deployment:
   - **Name**: `qr-code-api` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 0 main:app`
   - **Plan**: Free

## Step 3: Environment Variables

Add these environment variables in Render dashboard:

- `SESSION_SECRET`: Auto-generate a secure value
- `RENDER`: Set to `true` (this enables the keep-alive service)

## Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically deploy your app
3. You'll get a URL like: `https://your-app-name.onrender.com`

## Keep-Alive Feature

The app includes an automatic keep-alive service that:

- Only runs in production (when `RENDER` environment variable is set)
- Pings the `/health` endpoint every 5 minutes
- Prevents Render free tier from sleeping due to inactivity
- Logs all ping activities for monitoring

## Testing the Deployment

1. Visit your Render URL to see the demo interface
2. Test the API endpoints:
   - `GET /health` - Health check
   - `POST /api/v1/qr/url` - Generate QR codes
3. Check the logs in Render dashboard for keep-alive activity

## RapidAPI Integration

Once deployed, you can:

1. Register your API on RapidAPI Marketplace
2. Use your Render URL as the base URL
3. Import your API endpoints and documentation
4. Set up the pricing tiers as configured

## Files Created for Deployment

- `render.yaml` - Render deployment configuration
- `Procfile` - Process configuration for web service
- `runtime.txt` - Python version specification
- `keep_alive.py` - Keep-alive service to prevent sleeping
- `DEPLOYMENT.md` - This deployment guide

## Monitoring

- Monitor your app in Render dashboard
- Check logs for keep-alive pings every 5 minutes
- Use `/health` endpoint for external monitoring

## Important Notes

- Free Render services sleep after 15 minutes of inactivity
- The keep-alive service pings every 5 minutes to maintain activity
- Keep-alive only runs in production (not locally)
- Service starts 2 minutes after app deployment to allow initialization