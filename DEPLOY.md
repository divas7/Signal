# Deployment Guide

## 1. Backend Deployment (Render / Railway / Fly.io)

The backend is a FastAPI application using Poetry for dependency management.

### Environment Variables (Required)
Set these in your cloud provider's secrets manager:
- `KITE_API_KEY`: Your Zerodha API Key
- `UPSTOX_API_KEY`: Your Upstox API Key (Optional)
- `NEWS_API_KEY`: Your NewsAPI Key
- `DATABASE_URL`: Connection string for PostgreSQL
- `REDIS_URL`: Connection string for Redis

### Build Command
```bash
cd backend && poetry install && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
Or use the provided `Dockerfile`.

## 2. Frontend Deployment (Netlify / Vercel)

The frontend is a Next.js 14 application.

### Build Settings
- **Base Directory**: `frontend`
- **Build Command**: `next build` (or `npm run build`)
- **Publish Directory**: `.next`

### Environment Variables
- `NEXT_PUBLIC_API_URL`: URL of your deployed backend (e.g., `https://my-backend.onrender.com/api/v1`)
- `NEXT_PUBLIC_WS_URL`: WebSocket URL (e.g., `wss://my-backend.onrender.com/api/v1/signals/ws`)

## 3. Strict Live Data Policy
- Do not deploy with `mock_data=true` flags (not implemented to ensure compliance).
- Ensure the backend scheduler is running to fetch live data (configured in `app/main.py` startup events).
This app never generates synthetic market data. If a feed is down, signals are disabled or limited.
