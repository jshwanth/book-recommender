#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies from requirements.txt
pip install -r requirements.txt
echo "Dependencies installed."

# 2. Download the PRE-PROCESSED data file from Google Drive
# This completely skips running the complex notebook on the server.
# Replace YOUR_PKL_FILE_ID with the actual File ID from your Google Drive share link.
echo "Downloading pre-processed model data (recommender_data.pkl)..."
gdown --id 1izbbijtghBjTQ9z3-z5ekqUXkeMcpBG- -O recommender_data.pkl
echo "Model data downloaded successfully."

# 3. Run the database setup script to create the .db file
python database_setup.py
echo "Database initialized."

echo "Build finished successfully!"
