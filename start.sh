#!/bin/bash

echo "🚀 Starting Sentinel Wallet AI..."

# Start Nginx in background
echo "🌐 Starting Nginx..."
nginx -g "daemon off;" &

# Wait for Nginx to start
sleep 2
echo "✅ Nginx started"

# Start API server in foreground
echo "🤖 Starting API server..."
python api_server.py
