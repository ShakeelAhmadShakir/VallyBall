#!/bin/bash

echo "Stopping Gunicorn..."
pkill gunicorn

# Optionally wait and confirm it's stopped
sleep 2
if pgrep gunicorn > /dev/null; then
    echo "Gunicorn is still running, forcing kill..."
    pkill -9 gunicorn
else
    echo "Gunicorn stopped successfully."
fi
