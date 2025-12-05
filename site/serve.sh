#!/bin/bash
# Simple local server for testing the podcast site

echo "🚀 Starting local server on http://localhost:8000"
echo "📱 Note: podcast:// protocol links won't work locally"
echo "   You need to deploy to test subscription functionality"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 -m http.server 8000
