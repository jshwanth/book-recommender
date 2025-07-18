import sqlite3

# This script should be run only once to initialize the database.

# Connect to (or create) the database file
conn = sqlite3.connect('book_recommender.db')
cursor = conn.cursor()

print("Database connected successfully.")

# Create a table to store new user ratings
# Using 'IF NOT EXISTS' ensures this doesn't error if run multiple times
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    book_title TEXT NOT NULL,
    rating INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

print("Table 'user_ratings' created or already exists.")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete.")
