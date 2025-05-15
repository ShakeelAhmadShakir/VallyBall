#!/bin/bash

echo "Starting Gunicorn..."

# Activate virtual environment
source /home/ubuntu/env/bin/activate

# Navigate to your project directory
cd /home/ubuntu/football

# Start Gunicorn with the Unix socket
gunicorn football.wsgi:application \
  --bind unix:/run/gunicorn.sock \
  --workers 3 \
  --access-logfile /home/ubuntu/gunicorn-access.log \
  --error-logfile /home/ubuntu/gunicorn-error.log \
  --daemon

echo "Gunicorn started."
