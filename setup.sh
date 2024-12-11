#!/bin/bash

# If the venv directory does not exist, create it
if [ ! -d "venv" ]; then
    python3 -m venv venv
    venv/bin/pip install --upgrade pip
    venv/bin/pip install -r requirements.txt > /dev/null 2>&1 \
      && echo "Installed requirements" || echo "Failed to install requirements"
fi
