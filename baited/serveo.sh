#!/bin/bash

echo "🚀 Starting Flask Tracker..."
# Start Flask in background
python3 app.py &

# Wait for the server to start
sleep 3

# Serveo Subdomain (you can customize this)
SUBDOMAIN="baittracker"

# Start SSH tunnel in background and grab the public URL
echo "🌐 Connecting to Serveo..."
ssh -o StrictHostKeyChecking=no -R ${SUBDOMAIN}:80:localhost:5000 serveo.net > serveo_url.txt &

# Wait for Serveo to initialize
sleep 5

# Generate URLs
TRACK_URL="http://${SUBDOMAIN}.serveo.net/track/invoice"
DASHBOARD_URL="http://${SUBDOMAIN}.serveo.net/dashboard"

# Display and optionally copy
echo "🖼️ Tracking Image URL: $TRACK_URL"
echo "📊 Dashboard URL: $DASHBOARD_URL"

# Copy to clipboard if available
if command -v xclip >/dev/null 2>&1; then
    echo -n "$TRACK_URL" | xclip -selection clipboard
    echo "📋 Link copied to clipboard!"
else
    echo "ℹ️ Install xclip to enable automatic clipboard copy."
fi

# Tail Flask logs
echo "📝 Watching Flask logs..."
tail -f serveo_url.txt

