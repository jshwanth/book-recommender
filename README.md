# 📚 Book Recommender System

A **machine learning-based book recommendation system** that suggests books based on user preferences. Built using **Flask, Pandas, Scikit-learn, and Bootstrap**.

---

## 🚀 Features

- **Top 50 Popular Books** 📖  
- **Personalized Book Recommendations** 🎯  
- **Flask Backend with Jinja2 Templating** 🔥  
- **Bootstrap 5 for Responsive UI** 🎨  
- **Precomputed Recommendations for Fast Results** ⚡  

---

## 🛠️ Tech Stack

- **Backend:** Flask, Python, Pandas, Scikit-learn  
- **Frontend:** HTML, CSS, Bootstrap 5, Jinja2  
- **Database:** CSV Files (`Books.csv`, `Ratings.csv`, `Recommendations.csv`)  
- **Machine Learning:** Cosine Similarity for Book Recommendations  

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Book-Recommender-System.git
cd Book-Recommender-System
```

### 2️⃣ Install Dependencies
Ensure you have Python 3.7+ installed, then run

```bash
pip install -r requirements.txt
```

3️⃣ Run the Flask Application

```bash
python app.py
```

## ⚙️ How It Works

### **Data Processing**
- [x] Loads `Books.csv` and `Ratings.csv`.  
- [x] Creates a pivot table (User-Book matrix).  

### **Recommendation Algorithm**
- [x] Computes cosine similarity between books.  
- [x] Finds top 5 most similar books for each book.  

### **Flask Web Interface**
- [x] Displays results using Jinja2 & Bootstrap.  
