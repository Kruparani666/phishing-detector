🛡️ Phishing Email Detection Web Application

A Machine Learning based web application built using Flask that detects whether an email is:

✅ Legitimate

⚠ Spam

🚨 Phishing

The system includes authentication, prediction logging, analytics dashboard, and confusion matrix visualization.

🚀 Features
🔐 Authentication System

User Registration

Secure Login (Password Hashing)

Admin Role Management

🤖 Machine Learning

Trained NLP Model

TF-IDF Vectorization

Multi-class classification

Confidence percentage display

📊 Dashboard

Total predictions count

Legitimate / Spam / Phishing statistics

Model accuracy card

Prediction history table

Confidence percentage for each prediction

📈 Analytics

Confusion Matrix page

Visual classification performance

📁 Data Management

Prediction logs stored in SQLite

Export logs as CSV

Admin access to all logs

🏗️ Project Structure
project/
│
├── app.py
├── database.db
├── model/
│   ├── phishing_model.pkl
│   ├── vectorizer.pkl
│   ├── metrics.txt
│   └── confusion_matrix.npy
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── analytics.html
│
└── static/

🧠 Model Details

Algorithm: (e.g., Logistic Regression / Naive Bayes / etc.)

Feature Extraction: TF-IDF

Classes:

0 → Legitimate

1 → Spam

2 → Phishing

Accuracy is stored in:

model/metrics.txt


Confusion matrix stored in:

model/confusion_matrix.npy

⚙ Installation & Setup
1️⃣ Clone the Project
git clone <your-repo-url>
cd phishing-detection

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install flask flask_sqlalchemy flask_login scikit-learn numpy matplotlib

4️⃣ Run Application
python app.py


Open in browser:

http://127.0.0.1:5000

🗄 Database

If you modify the database model:

Delete:

database.db


Then restart app:

python app.py


Database will auto-create.

📊 Routes
Route	Description
/	Home page
/register	User registration
/login	Login page
/dashboard	User dashboard
/analytics	Confusion matrix page
/predict	Email classification
/logout	Logout
🔒 Security Features

Password hashing using Werkzeug

Role-based access (User / Admin)

Protected routes using Flask-Login

🎯 Future Improvements

ROC Curve Visualization

Precision / Recall / F1 Score Page

Live AJAX Prediction

Chart.js Analytics

Dark Mode UI

Docker Deployment

Cloud Deployment (AWS / Render)

👨‍💻 Author

Developed as a Machine Learning + Cybersecurity Web Application Project.
