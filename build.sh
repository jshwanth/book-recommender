#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies from requirements.txt
pip install -r requirements.txt
echo "Dependencies installed."

# 2. Download the data files from Google Drive using gdown
#    This method correctly handles large file warnings from Google Drive.
#    Replace YOUR_FILE_ID_HERE with the actual File ID from your Google Drive share link.
echo "Downloading data files from Google Drive..."
gdown --id 15Hig5IxFDW1xYBPdJnXLshzvMlNWV22a-RMiSMAmUkE -O Books.csv
gdown --id 126e2ukj6Y2HCixm7a3p342L3PkqvT7X89MNzKuTeJi0 -O Ratings.csv
gdown --id 1mcKKeoXstL3960iw6pj14UB__oUdNqEmG9aTWfeFPHs -O Users.csv
echo "Data files downloaded successfully."

# 3. Run the Jupyter Notebook to generate the data file
# This command executes the notebook and creates recommender_data.pkl
jupyter nbconvert --to notebook --execute book-recommender.ipynb
echo "Jupyter Notebook executed, recommender_data.pkl created."

# 4. Run the database setup script to create the .db file
python database_setup.py
echo "Database initialized."

echo "Build finished successfully!"
