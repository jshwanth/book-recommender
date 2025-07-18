#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

echo "Dependencies installed."

# 2. Run the Jupyter Notebook to generate the data file
# This command executes the notebook and creates recommender_data.pkl
jupyter nbconvert --to notebook --execute book-recommender.ipynb

echo "Jupyter Notebook executed, recommender_data.pkl created."

# 3. Run the database setup script
python database_setup.py

echo "Database initialized."

echo "Build finished successfully!"