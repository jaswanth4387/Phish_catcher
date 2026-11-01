# 🎣 Phish Catcher

A Django web application that detects **phishing URLs** using machine learning. Registered users submit a URL and get an instant verdict, while a service provider (admin) can view users and predictions, compare four ML algorithms on accuracy, explore charts, and export results to Excel.

**Live demo:** https://phish-catcher.onrender.com

---
## ✨ Features

### Remote User
- Register and log in (passwords are hashed with Django's `make_password`)
- View personal profile
- Submit a URL and get **"No Phishing Attack"** or **"Phishing Attack Detected"**
- Every prediction is stored in the database

### Service Provider (Admin)
- Dedicated provider login
- **View Remote Users**: list of all registered users
- **View Predictions**: every URL checked and its result
- **Attack Ratio**: percentage of safe vs. phishing predictions
- **Train & Compare Models**: trains four classifiers and records the test accuracy of each
- **Charts**: pie, bar, line and other chart types for ratio and accuracy data
- **Download Predictions** as an Excel (`.xls`) file

---

## 🧠 Machine Learning

| Item | Detail |
|------|--------|
| Dataset | `Datasets.csv`, about 22.9K labelled URLs (~15.4K legitimate, ~7.5K phishing) |
| Labels | `0` = legitimate, `1` = phishing |
| Features | Bag-of-words over the URL string (`CountVectorizer`) |
| Split | 80% train / 20% test |
| Prediction model | Multinomial Naive Bayes |

**Algorithms compared on the Train Model page:**

1. Naive Bayes (`MultinomialNB`)
2. Support Vector Machine (`LinearSVC`)
3. Logistic Regression
4. Decision Tree

Accuracy for each is saved to the database and shown in the charts.

---

## 🛠 Tech Stack

- **Backend:** Python, Django 6
- **ML:** scikit-learn, pandas, numpy
- **Database:** SQLite locally; PostgreSQL via `DATABASE_URL` (`dj-database-url`, `psycopg2-binary`)
- **Static files / deployment:** WhiteNoise, Gunicorn
- **Export:** xlwt (Excel)

---

## 📁 Project Structure

```
phish_catcher/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── phish_catcher/          # Project settings, root URLs, WSGI/ASGI
├── User/                   # Remote-user app
│   ├── models.py           # ClientRegister_Model, attack_prediction,
│   │                       # detection_accuracy, detection_ratio
│   ├── views.py            # Register, login, profile, URL prediction
│   └── Datasets.csv
├── Provider/               # Service-provider app
│   ├── views.py            # Users, predictions, ratio, charts, training, export
│   ├── urls.py
│   └── Datasets.csv
└── templates/html/
    ├── RUser/              # User-facing pages
    └── SProvider/          # Provider pages
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+ (required by Django 6)
- pip

### Installation

```bash
# 1. Clone
git clone https://github.com/jaswanth4387/Phish_catcher.git
cd Phish_catcher

# 2. Virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Run
python manage.py runserver
```

Open http://127.0.0.1:8000/.

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `SECRET_KEY` | Django secret key | insecure fallback (change it!) |
| `DEBUG` | Set to `True` for local development | off |
| `DATABASE_URL` | PostgreSQL connection string | local SQLite |

Example for local development:

```bash
export DEBUG=True
export SECRET_KEY="your-long-random-string"
```

---

## 🗺 Routes

| Route | Who | Purpose |
|-------|-----|---------|
| `/` | Public | Home |
| `/Register1/` | Public | User registration |
| `/login/` | Public | User login |
| `/ViewYourProfile/` | User | Profile |
| `/Predict_Web_Spoofing_Attack_Type/` | Public | URL prediction |
| `/serviceproviderlogin/` | Provider | Provider login |
| `/View_Remote_Users/` | Provider | All users |
| `/View_Prediction_Of_Web_Spoofing_Attack_Status/` | Provider | All predictions |
| `/View_Web_Spoofing_Attack_Status_Ratio/` | Provider | Safe vs. phishing ratio |
| `/train_model/` | Provider | Train and compare models |
| `/charts/<type>/`, `/charts1/<type>/`, `/likeschart/<type>/` | Provider | Charts |
| `/Download_Trained_DataSets/` | Provider | Excel export |

---

## ⚠️ Known Limitations & Roadmap

- [ ] **Provider authentication:** the login uses a fixed placeholder credential and provider pages have no access check. Replace with Django auth and a role or permission check.
- [ ] **Prediction page requires no login**, and the model is **retrained on every request**. Train once, save the model with `joblib`, and load it at startup for fast, consistent results.
- [ ] **Case-sensitive path bug:** `Provider/views.py` looks for `provider/Datasets.csv` (lowercase), but the folder is `Provider`. This fails on Linux hosts such as Render.
- [ ] **`dashboard` view has no route or template** yet.
- [ ] Set `ALLOWED_HOSTS` to your real domain instead of `*`.
- [ ] Keep one copy of `Datasets.csv` (the two folders hold identical files).
- [ ] Add tests, URL-based features (length, special characters, TLD), and a REST API.

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit and push your changes
4. Open a Pull Request

---

## 👤 Author

**Jakkampudi Jaswanth Krishna**
GitHub: [@jaswanth4387](https://github.com/jaswanth4387)

---

