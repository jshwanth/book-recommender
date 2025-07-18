# Advanced Hybrid Book Recommender System

This is a full-stack web application that provides book recommendations using a sophisticated hybrid model, combining both Collaborative and Content-Based Filtering techniques.

![alt text](image.png)

**Live Demo:** [Link to your deployed app on Render/PythonAnywhere] <-- *This is the most important link!*

## Features

* **Hybrid Recommendation Engine:** Combines two distinct models for robust and diverse suggestions:
    * **Collaborative Filtering:** Recommends books based on the principle "users who liked this book also liked...".
    * **Content-Based Filtering:** Recommends books by matching content attributes like author and publisher.
* **Interactive UI:** A clean and modern interface built with Flask and Tailwind CSS allows users to easily select a book and a model type.
* **User Feedback Loop:** Users can rate recommended books. These ratings are stored in an SQLite database, creating a foundation for a truly personalized system.
* **Model Evaluation:** The collaborative filtering model's performance was validated using offline evaluation, calculating Precision@k and Recall@k metrics to ensure recommendation quality.

## How It Works

The project is divided into two main parts:

1.  **Offline Model Training (`book-recommender.ipynb`):** A Jupyter Notebook handles all the heavy data processing, including cleaning the data, building the user-item matrix, training the TF-IDF vectorizer, and calculating the similarity matrices for both models. The notebook concludes by exporting all necessary Python objects into a single `recommender_data.pkl` file and running the evaluation metrics.
2.  **Flask Web Application (`main.py`):** The web server loads the pre-computed models from the `.pkl` file. It handles user requests, serves the HTML templates, and manages the SQLite database for user ratings.

## How to Run This Project Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jshwanth/book-recommender
    cd book-recommender
    ```
2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Download the data:**
    Download the Book-Crossing dataset from [this Kaggle link](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset?resource=download) and place the `Books.csv`, `Ratings.csv`, and `Users.csv` files in the root of the project folder.
5.  **Run the Jupyter Notebook:**
    Open and run all cells in `book-recommender.ipynb` to generate the `recommender_data.pkl` file.
6.  **Set up the database:**
    Run the setup script once to create the database file.
    ```bash
    python database_setup.py
    ```
7.  **Run the Flask app:**
    ```bash
    python main.py
    ```
8.  Open your browser and go to `http://127.0.0.1:5000`.

## Technologies Used

* **Backend:** Python, Flask
* **Data Science:** Pandas, NumPy, Scikit-learn
* **Database:** SQLite
* **Frontend:** HTML, Tailwind CSS