from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load popular books
try:
    popular_df = pd.read_csv("popular.csv")
    print("Loaded popular.csv successfully!")
except FileNotFoundError:
    print("Error: popular.csv not found!")
    popular_df = pd.DataFrame()  # Empty DataFrame to prevent errors

# Load books data
try:
    books = pd.read_csv("Books.csv", low_memory=False)
except FileNotFoundError:
    print("Error: Books.csv not found!")
    books = pd.DataFrame()

# Load recommendations from CSV
# Load recommendations from CSV
try:
    recommendations_df = pd.read_csv("recommendations.csv")
    print("Loaded recommendations.csv successfully!")
    print(recommendations_df.head())  # Print first 5 rows for debugging
except FileNotFoundError:
    print("Error: recommendations.csv not found!")
    recommendations_df = pd.DataFrame()


# Function to get recommendations from recommendations.csv
def get_similar_books(book_title, num_recommendations=5):
    if recommendations_df.empty:
        print("Error: recommendations.csv is empty!")
        return []

    print(f"Searching for recommendations for: {book_title}")
    print("Available Books in CSV:", recommendations_df["Book-Title"].unique()[:10])  # Print first 10 unique titles

    # Filter the recommendations based on the selected book
    book_recommendations = recommendations_df[recommendations_df["Book-Title"].str.lower() == book_title.lower()]

    # Select the top N recommendations
    recommended_books = book_recommendations.head(num_recommendations).to_dict(orient="records")

    return recommended_books


@app.route("/")
def index():
    return render_template("index.html",
                           book_name=list(popular_df.get('Book-Title', [])),
                           author=list(popular_df.get('Book-Author_x', [])),
                           image=list(popular_df.get('Image-URL-L_x', [])),
                           rating=list(popular_df.get('average_rating', [])),
                           number_rating=list(popular_df.get('number_rating', []))
                           )

@app.route("/recommend")
def recommend():
    return render_template("recommender.html")

@app.route("/recommend_button", methods=["POST"])
def recommend_button():
    user_input = request.form.get("user_input")
    recommendations = get_similar_books(user_input)

    if not recommendations:
        return render_template("recommender.html", recommendations=[], user_input=user_input, error="No recommendations found!")

    return render_template("recommender.html", recommendations=recommendations, user_input=user_input)


if __name__ == "__main__":
    app.run(debug=True)
