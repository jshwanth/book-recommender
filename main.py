from flask import Flask, render_template, request, session, redirect, url_for, flash
import pickle
import numpy as np
import pandas as pd
import sqlite3
import uuid

# --- Load Data ---
try:
    recommender_data = pickle.load(open('recommender_data.pkl', 'rb'))
except FileNotFoundError:
    print("ERROR: recommender_data.pkl not found. Please run the Jupyter Notebook first.")
    exit()

popular_df = recommender_data['popular_df']
pt = recommender_data['pt']
books = recommender_data['books']
collaborative_similarity_scores = recommender_data['collaborative_similarity_scores']
content_df = recommender_data['content_df']
content_similarity_scores = recommender_data['content_similarity_scores']
all_book_titles = pt.index.tolist()

app = Flask(__name__)
# A secret key is needed to securely sign the session cookie
app.secret_key = 'a_random_super_secret_key'

# --- Database Helper ---
def get_db_connection():
    conn = sqlite3.connect('book_recommender.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Recommendation Logic ---
def recommend_collaborative(book_title):
    try:
        index = np.where(pt.index == book_title)[0][0]
        similar_items = sorted(list(enumerate(collaborative_similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:7] # Get 6 to be safe
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['title'] == pt.index[i[0]]]
            if not temp_df.empty:
                item.extend(list(temp_df.drop_duplicates('title')['title'].values))
                item.extend(list(temp_df.drop_duplicates('title')['author'].values))
                item.extend(list(temp_df.drop_duplicates('title')['image_url'].values))
                data.append(item)
        return data
    except IndexError: return []

def recommend_content(book_title):
    try:
        book_index = content_df[content_df['title'] == book_title].index[0]
        distances = content_similarity_scores[book_index]
        books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7] # Get 6 to be safe
        data = []
        for i in books_list:
            item = []
            rec_book_title = content_df.iloc[i[0]].title
            temp_df = books[books['title'] == rec_book_title]
            if not temp_df.empty:
                item.extend(list(temp_df.drop_duplicates('title')['title'].values))
                item.extend(list(temp_df.drop_duplicates('title')['author'].values))
                item.extend(list(temp_df.drop_duplicates('title')['image_url'].values))
                data.append(item)
        return data
    except (IndexError, KeyError): return []

def recommend_hybrid(book_title):
    collab_recs = recommend_collaborative(book_title)
    content_recs = recommend_content(book_title)
    hybrid_recs, seen_titles = [], set()
    
    # Add the selected book to seen_titles to avoid recommending it to itself
    seen_titles.add(book_title)

    len_collab = len(collab_recs)
    len_content = len(content_recs)
    max_len = max(len_collab, len_content)

    for i in range(max_len):
        if i < len_collab:
            rec = collab_recs[i]
            if rec and len(rec) > 0 and rec[0] not in seen_titles:
                hybrid_recs.append(rec)
                seen_titles.add(rec[0])
        
        if i < len_content:
            rec = content_recs[i]
            if rec and len(rec) > 0 and rec[0] not in seen_titles:
                hybrid_recs.append(rec)
                seen_titles.add(rec[0])
                
    return hybrid_recs[:5]

# --- Web Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    conn = get_db_connection()
    user_ratings_cursor = conn.execute('SELECT book_title, rating FROM user_ratings WHERE session_id = ?',
                                     (session['session_id'],)).fetchall()
    conn.close()
    user_ratings = {row['book_title']: row['rating'] for row in user_ratings_cursor}

    recommendations, error_message, selected_book = [], None, None
    model_type = 'hybrid'

    if request.method == 'POST':
        selected_book = request.form.get('user_input')
        model_type = request.form.get('model_type')
        if not selected_book:
            error_message = "Please select a book."
        else:
            if model_type == 'collaborative': recommendations = recommend_collaborative(selected_book)
            elif model_type == 'content': recommendations = recommend_content(selected_book)
            elif model_type == 'hybrid': recommendations = recommend_hybrid(selected_book)
            
            if not recommendations and selected_book:
                error_message = f"Sorry, no recommendations found for '{selected_book}'."

    return render_template('index.html',
                           popular_books=popular_df.to_dict(orient='records'),
                           all_book_titles=all_book_titles,
                           recommendations=recommendations,
                           error_message=error_message,
                           selected_book=selected_book,
                           selected_model=model_type,
                           user_ratings=user_ratings)

@app.route('/rate_book', methods=['POST'])
def rate_book():
    book_title = request.form.get('book_title')
    rating_str = request.form.get('rating')
    session_id = session.get('session_id')

    if book_title and rating_str and session_id:
        try:
            rating = int(rating_str)
            conn = get_db_connection()
            existing_rating = conn.execute('SELECT id FROM user_ratings WHERE session_id = ? AND book_title = ?', 
                                           (session_id, book_title)).fetchone()
            if existing_rating:
                conn.execute('UPDATE user_ratings SET rating = ? WHERE id = ?', (rating, existing_rating['id']))
                flash(f"Successfully updated your rating for '{book_title}' to {rating}/10!", 'success')
            else:
                conn.execute('INSERT INTO user_ratings (session_id, book_title, rating) VALUES (?, ?, ?)',
                             (session_id, book_title, rating))
                flash(f"Successfully rated '{book_title}' a {rating}/10!", 'success')
            conn.commit()
            conn.close()
        except (ValueError, sqlite3.Error) as e:
            print(f"Error rating book: {e}")
            flash(f"Error rating book. Please try again.", 'error')
            
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
